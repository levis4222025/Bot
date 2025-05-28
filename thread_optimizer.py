"""
Thread optimizer for the BGMI Warrior Bot by IBR.
Dynamically adjusts thread values based on performance.
"""
import logging
import time
from typing import Dict, List, Tuple, Optional

class ThreadOptimizer:
    """Service for optimizing thread values based on performance metrics"""
    
    def __init__(self, min_threads: int = 50, max_threads: int = 500):
        """Initialize thread optimizer"""
        self.min_threads = min_threads
        self.max_threads = max_threads
        self.performance_history = {}
        self.logger = logging.getLogger('bgmi_warrior_bot.thread_optimizer')
        
    def record_performance(self, user_id: int, thread_value: int, 
                          ip: str, port: int, success: bool, duration: float):
        """Record performance data for a user's action"""
        if user_id not in self.performance_history:
            self.performance_history[user_id] = []
            
        # Keep history limited to last 10 entries
        history = self.performance_history[user_id]
        history.append({
            'thread_value': thread_value,
            'ip': ip,
            'port': port,
            'success': success,
            'duration': duration,
            'timestamp': time.time()
        })
        
        # Trim history
        if len(history) > 10:
            self.performance_history[user_id] = history[-10:]
            
    def get_optimal_thread_value(self, user_id: int, default: int = 200) -> int:
        """Get optimal thread value based on user's history"""
        if user_id not in self.performance_history or not self.performance_history[user_id]:
            return default
            
        history = self.performance_history[user_id]
        
        # Filter by success
        successful = [entry for entry in history if entry['success']]
        if not successful:
            return default
            
        # Find the thread value with best performance
        best_thread = max(successful, key=lambda x: x['duration'])['thread_value']
        
        # Apply bounds
        return max(min(best_thread, self.max_threads), self.min_threads)
        
    def suggest_adjustment(self, user_id: int, current_thread: int) -> Optional[int]:
        """Suggest thread adjustment based on history"""
        if user_id not in self.performance_history or len(self.performance_history[user_id]) < 3:
            return None
            
        history = self.performance_history[user_id]
        
        # Check for any failures
        failures = [entry for entry in history if not entry['success']]
        if failures:
            # Reduce threads by 10% if there are failures
            suggested = int(current_thread * 0.9)
            self.logger.info(f"Suggesting thread reduction for user {user_id}: {current_thread} -> {suggested}")
            return max(self.min_threads, suggested)
        
        # Check if performance is improving with higher threads
        sorted_history = sorted(history, key=lambda x: x['timestamp'])
        if sorted_history[-1]['thread_value'] > sorted_history[0]['thread_value']:
            # If using more threads has been working, suggest a 5% increase
            suggested = int(current_thread * 1.05)
            self.logger.info(f"Suggesting thread increase for user {user_id}: {current_thread} -> {suggested}")
            return min(self.max_threads, suggested)
            
        return None