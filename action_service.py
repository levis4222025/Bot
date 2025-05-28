"""
Service for handling the strike actions in BGMI Warrior Bot by IBR.
Provides asynchronous execution of process actions.
"""
import asyncio
import logging
import os
import signal
import time
from datetime import datetime
from typing import Dict, Optional, Tuple, Any, List

import pytz

from models import UserAction, UserMode

logger = logging.getLogger('bgmi_warrior_bot.action_service')

class ActionService:
    """Service for handling strike actions"""
    
    def __init__(self, action_path: str = "./action"):
        """Initialize action service"""
        self.action_path = action_path
        self.active_processes: Dict[int, Dict[str, Any]] = {}
        
        # Verify action binary exists and is executable
        if not os.path.isfile(self.action_path) or not os.access(self.action_path, os.X_OK):
            logger.error(f"Action binary not found or not executable at {self.action_path}")
            raise FileNotFoundError(f"Action binary not found or not executable at {self.action_path}")
    
    async def start_action(self, user_id: int, ip: str, port: int, 
                          duration: int, thread_value: int = 200) -> Tuple[bool, str, Optional[UserAction]]:
        """Start an action process"""
        try:
            # Create action object
            action = UserAction(
                user_id=user_id,
                ip=ip,
                port=port,
                duration=duration,
                mode=UserMode.AUTO if duration > 100 else UserMode.MANUAL,
                thread_value=thread_value
            )
            
            # Start the process
            process = await asyncio.create_subprocess_exec(
                self.action_path, ip, str(port), str(duration), str(thread_value),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Store process info
            self.active_processes[user_id] = {
                'process': process,
                'ip': ip,
                'port': port,
                'duration': duration,
                'start_time': datetime.now(pytz.utc),
                'action_id': action.id
            }
            
            logger.info(f"Started action for user {user_id}: IP {ip}, port {port}, duration {duration}s")
            return True, "Action started successfully", action
            
        except Exception as e:
            error_msg = f"Failed to start action: {str(e)}"
            logger.error(f"Error starting action for user {user_id}: {error_msg}")
            return False, error_msg, None
    
    async def stop_action(self, user_id: int) -> Tuple[bool, str]:
        """Stop an action process"""
        if user_id not in self.active_processes:
            return False, "No active process found"
            
        try:
            process_info = self.active_processes[user_id]
            process = process_info['process']
            
            # Check if process is still running
            if process.returncode is None:
                # Try graceful termination first
                process.terminate()
                
                # Wait for process to terminate
                try:
                    await asyncio.wait_for(process.wait(), timeout=3.0)
                except asyncio.TimeoutError:
                    # Force kill if it doesn't terminate
                    try:
                        process.kill()
                    except ProcessLookupError:
                        pass
                
                logger.info(f"Stopped action for user {user_id}")
                del self.active_processes[user_id]
                return True, "Action stopped successfully"
            else:
                # Process already completed
                del self.active_processes[user_id]
                return False, "Process already completed"
                
        except Exception as e:
            error_msg = f"Error stopping action: {str(e)}"
            logger.error(f"Error stopping action for user {user_id}: {error_msg}")
            return False, error_msg
    
    async def stop_all_actions(self) -> int:
        """Stop all running actions"""
        stopped_count = 0
        user_ids = list(self.active_processes.keys())
        
        for user_id in user_ids:
            success, _ = await self.stop_action(user_id)
            if success:
                stopped_count += 1
                
        return stopped_count
    
    async def get_action_status(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get status of user's action"""
        if user_id not in self.active_processes:
            return None
            
        process_info = self.active_processes[user_id]
        process = process_info['process']
        
        # Check if process is still running
        if process.returncode is None:
            start_time = process_info['start_time']
            elapsed = (datetime.now(pytz.utc) - start_time).total_seconds()
            remaining = process_info['duration'] - elapsed
            
            return {
                'status': 'running',
                'ip': process_info['ip'],
                'port': process_info['port'],
                'duration': process_info['duration'],
                'elapsed': elapsed,
                'remaining': max(0, remaining),
                'percent_complete': min(100, (elapsed / process_info['duration']) * 100)
            }
        else:
            # Process completed or failed
            return {
                'status': 'completed' if process.returncode == 0 else 'failed',
                'ip': process_info['ip'],
                'port': process_info['port'],
                'duration': process_info['duration'],
                'returncode': process.returncode
            }
    
    async def monitor_action(self, user_id: int, 
                           update_callback=None, 
                           completion_callback=None):
        """Monitor action process with updates and completion notification"""
        if user_id not in self.active_processes:
            return
            
        process_info = self.active_processes[user_id]
        process = process_info['process']
        total_duration = process_info['duration']
        
        # Monitor until process completes
        while process.returncode is None:
            # Check if process is still running
            if user_id not in self.active_processes:
                break
                
            elapsed = (datetime.now(pytz.utc) - process_info['start_time']).total_seconds()
            remaining = max(0, total_duration - elapsed)
            
            # Call update callback if provided
            if update_callback:
                try:
                    await update_callback(user_id, elapsed, remaining)
                except Exception as e:
                    logger.error(f"Error in update callback: {str(e)}")
            
            # Check if process completed
            if remaining <= 0 or process.returncode is not None:
                break
                
            # Wait before checking again
            await asyncio.sleep(min(5, remaining))
        
        # Process output
        try:
            stdout, stderr = await process.communicate()
            stdout_text = stdout.decode().strip() if stdout else ""
            stderr_text = stderr.decode().strip() if stderr else ""
            
            # Determine exit status
            success = process.returncode == 0
            
            logger.info(f"Action completed for user {user_id}, success: {success}")
            
            # Call completion callback if provided
            if completion_callback:
                try:
                    await completion_callback(
                        user_id, 
                        success, 
                        stdout_text, 
                        stderr_text,
                        process_info
                    )
                except Exception as e:
                    logger.error(f"Error in completion callback: {str(e)}")
            
            # Clean up
            if user_id in self.active_processes:
                del self.active_processes[user_id]
                
        except Exception as e:
            logger.error(f"Error completing action for user {user_id}: {str(e)}")
            
            # Clean up on error
            if user_id in self.active_processes:
                del self.active_processes[user_id]