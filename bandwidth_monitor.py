"""
Bandwidth monitor for the BGMI Warrior Bot by IBR.
Tracks system bandwidth usage and limits actions if needed.
"""
import asyncio
import logging
import psutil
import time
from typing import Dict, Tuple, Optional

class BandwidthMonitor:
    """Service for monitoring system bandwidth usage"""
    
    def __init__(self, max_bandwidth_mbps: float = 100.0, check_interval: int = 5):
        """Initialize bandwidth monitor"""
        self.max_bandwidth_mbps = max_bandwidth_mbps
        self.check_interval = check_interval
        self.last_bytes_sent = 0
        self.last_bytes_recv = 0
        self.last_check_time = 0
        self.current_usage_mbps = 0.0
        self.is_monitoring = False
        self.logger = logging.getLogger('bgmi_warrior_bot.bandwidth_monitor')
        
    async def start_monitoring(self):
        """Start bandwidth monitoring"""
        self.is_monitoring = True
        self.logger.info(f"Starting bandwidth monitoring (max: {self.max_bandwidth_mbps} Mbps)")
        
        # Initialize counters
        net_io = psutil.net_io_counters()
        self.last_bytes_sent = net_io.bytes_sent
        self.last_bytes_recv = net_io.bytes_recv
        self.last_check_time = time.time()
        
        # Start monitoring loop
        while self.is_monitoring:
            await self._check_bandwidth()
            await asyncio.sleep(self.check_interval)
            
    async def stop_monitoring(self):
        """Stop bandwidth monitoring"""
        self.is_monitoring = False
        self.logger.info("Stopping bandwidth monitoring")
        
    async def _check_bandwidth(self):
        """Check current bandwidth usage"""
        try:
            # Get current network stats
            net_io = psutil.net_io_counters()
            bytes_sent = net_io.bytes_sent
            bytes_recv = net_io.bytes_recv
            current_time = time.time()
            
            # Calculate bandwidth usage
            time_diff = current_time - self.last_check_time
            bytes_sent_diff = bytes_sent - self.last_bytes_sent
            bytes_recv_diff = bytes_recv - self.last_bytes_recv
            
            # Calculate Mbps (both directions)
            mbps_sent = (bytes_sent_diff * 8) / (time_diff * 1_000_000)
            mbps_recv = (bytes_recv_diff * 8) / (time_diff * 1_000_000)
            total_mbps = mbps_sent + mbps_recv
            
            # Update state
            self.current_usage_mbps = total_mbps
            self.last_bytes_sent = bytes_sent
            self.last_bytes_recv = bytes_recv
            self.last_check_time = current_time
            
            if total_mbps > self.max_bandwidth_mbps * 0.8:
                self.logger.warning(f"High bandwidth usage: {total_mbps:.2f} Mbps")
                
        except Exception as e:
            self.logger.error(f"Error checking bandwidth: {str(e)}")
            
    def can_start_new_action(self) -> Tuple[bool, float]:
        """Check if a new action can be started based on bandwidth usage"""
        if not self.is_monitoring:
            return True, 0.0
            
        # Allow if bandwidth usage is under 80% of max
        available_percentage = (self.max_bandwidth_mbps - self.current_usage_mbps) / self.max_bandwidth_mbps * 100
        can_start = self.current_usage_mbps < (self.max_bandwidth_mbps * 0.8)
        
        return can_start, available_percentage
        
    def get_bandwidth_stats(self) -> Dict[str, float]:
        """Get current bandwidth statistics"""
        return {
            'current_usage_mbps': self.current_usage_mbps,
            'max_bandwidth_mbps': self.max_bandwidth_mbps,
            'usage_percent': (self.current_usage_mbps / self.max_bandwidth_mbps) * 100,
            'last_check_time': self.last_check_time
        }