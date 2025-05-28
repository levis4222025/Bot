"""
Analytics module for the BGMI Warrior Bot by IBR.
Generates usage statistics and performance metrics.
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
from io import BytesIO

from database import Database

logger = logging.getLogger('bgmi_warrior_bot.analytics')

class Analytics:
    """Analytics service for generating insights and statistics"""
    
    def __init__(self, db: Database, timezone: str):
        """Initialize analytics service"""
        self.db = db
        self.timezone = pytz.timezone(timezone)
    
    async def generate_usage_report(self, days: int = 7) -> BytesIO:
        """Generate usage report chart as image"""
        try:
            stats = await self.db.get_action_stats_by_day(days)
            
            # Convert to pandas DataFrame
            df = pd.DataFrame(stats)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # Create plot
            plt.figure(figsize=(10, 6))
            plt.bar(df['date'], df['count'], color='blue')
            plt.title(f'BGMI Warrior Bot by IBR - Action Count (Last {days} Days)')
            plt.xlabel('Date')
            plt.ylabel('Number of Actions')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save plot to buffer
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()
            
            return buf
            
        except Exception as e:
            logger.error(f"Error generating usage report: {str(e)}", exc_info=True)
            return None
    
    async def generate_user_heatmap(self, days: int = 7) -> BytesIO:
        """Generate user activity heatmap"""
        try:
            hourly_data = await self.db.get_hourly_action_stats(days)
            
            # Create 24x7 matrix for the heatmap (hour x day)
            heatmap_data = np.zeros((24, 7))
            
            # Fill data
            for entry in hourly_data:
                day_of_week = entry['day_of_week']
                hour = entry['hour']
                count = entry['count']
                heatmap_data[hour, day_of_week] = count
            
            # Create plot
            fig, ax = plt.subplots(figsize=(10, 8))
            im = ax.imshow(heatmap_data, cmap='viridis')
            
            # Set labels
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            hours = [f'{h:02d}:00' for h in range(24)]
            
            ax.set_xticks(np.arange(len(days)))
            ax.set_yticks(np.arange(len(hours)))
            ax.set_xticklabels(days)
            ax.set_yticklabels(hours)
            
            plt.colorbar(im, ax=ax, label='Number of Actions')
            plt.title('User Activity Heatmap by Hour and Day')
            plt.tight_layout()
            
            # Save plot to buffer
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()
            
            return buf
            
        except Exception as e:
            logger.error(f"Error generating user heatmap: {str(e)}", exc_info=True)
            return None
            
    async def get_top_users(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top users by action count"""
        return await self.db.get_top_users_by_actions(limit)
    
    async def get_user_usage_trend(self, user_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """Get usage trend for a specific user"""
        return await self.db.get_user_action_history(user_id, days)