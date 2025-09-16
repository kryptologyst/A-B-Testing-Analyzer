"""
Mock Database for A/B Testing Analyzer
Provides sample datasets for testing and demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class MockABDatabase:
    """
    Mock database containing various A/B test scenarios for demonstration
    """
    
    def __init__(self):
        self.experiments = {}
        self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Generate realistic A/B test datasets"""
        
        # Experiment 1: E-commerce checkout button color
        self.experiments['checkout_button_color'] = {
            'name': 'Checkout Button Color Test',
            'description': 'Testing red vs blue checkout button for conversion rate',
            'start_date': '2024-01-15',
            'end_date': '2024-02-15',
            'status': 'completed',
            'metric_type': 'conversion_rate',
            'control': {
                'name': 'Blue Button (Control)',
                'visitors': 5420,
                'conversions': 487,
                'conversion_rate': 0.0899
            },
            'test': {
                'name': 'Red Button (Test)',
                'visitors': 5380,
                'conversions': 534,
                'conversion_rate': 0.0993
            }
        }
        
        # Experiment 2: Email subject line
        self.experiments['email_subject_line'] = {
            'name': 'Email Subject Line Test',
            'description': 'Testing personalized vs generic email subject lines',
            'start_date': '2024-02-01',
            'end_date': '2024-02-28',
            'status': 'completed',
            'metric_type': 'conversion_rate',
            'control': {
                'name': 'Generic Subject (Control)',
                'visitors': 12500,
                'conversions': 875,
                'conversion_rate': 0.0700
            },
            'test': {
                'name': 'Personalized Subject (Test)',
                'visitors': 12480,
                'conversions': 1023,
                'conversion_rate': 0.0820
            }
        }
        
        # Experiment 3: Landing page layout
        self.experiments['landing_page_layout'] = {
            'name': 'Landing Page Layout Test',
            'description': 'Testing single-column vs two-column layout',
            'start_date': '2024-03-01',
            'end_date': '2024-03-31',
            'status': 'running',
            'metric_type': 'conversion_rate',
            'control': {
                'name': 'Single Column (Control)',
                'visitors': 3200,
                'conversions': 256,
                'conversion_rate': 0.0800
            },
            'test': {
                'name': 'Two Column (Test)',
                'visitors': 3180,
                'conversions': 235,
                'conversion_rate': 0.0739
            }
        }
        
        # Experiment 4: Pricing strategy
        self.experiments['pricing_strategy'] = {
            'name': 'Pricing Strategy Test',
            'description': 'Testing $9.99 vs $10.00 pricing',
            'start_date': '2024-02-15',
            'end_date': '2024-03-15',
            'status': 'completed',
            'metric_type': 'conversion_rate',
            'control': {
                'name': '$10.00 (Control)',
                'visitors': 8900,
                'conversions': 623,
                'conversion_rate': 0.0700
            },
            'test': {
                'name': '$9.99 (Test)',
                'visitors': 8850,
                'conversions': 708,
                'conversion_rate': 0.0800
            }
        }
        
        # Experiment 5: Mobile app onboarding
        self.experiments['mobile_onboarding'] = {
            'name': 'Mobile App Onboarding Test',
            'description': 'Testing 3-step vs 5-step onboarding process',
            'start_date': '2024-01-01',
            'end_date': '2024-01-31',
            'status': 'completed',
            'metric_type': 'conversion_rate',
            'control': {
                'name': '5-Step Onboarding (Control)',
                'visitors': 15600,
                'conversions': 2340,
                'conversion_rate': 0.1500
            },
            'test': {
                'name': '3-Step Onboarding (Test)',
                'visitors': 15580,
                'conversions': 2804,
                'conversion_rate': 0.1800
            }
        }
    
    def get_experiment(self, experiment_id):
        """Get a specific experiment by ID"""
        return self.experiments.get(experiment_id)
    
    def list_experiments(self):
        """List all available experiments"""
        return list(self.experiments.keys())
    
    def get_experiment_summary(self):
        """Get a summary of all experiments"""
        summary = []
        for exp_id, exp_data in self.experiments.items():
            summary.append({
                'id': exp_id,
                'name': exp_data['name'],
                'status': exp_data['status'],
                'start_date': exp_data['start_date'],
                'end_date': exp_data['end_date'],
                'control_rate': exp_data['control']['conversion_rate'],
                'test_rate': exp_data['test']['conversion_rate']
            })
        return summary
    
    def generate_detailed_data(self, experiment_id, include_timestamps=True):
        """
        Generate detailed user-level data for an experiment
        
        Args:
            experiment_id (str): ID of the experiment
            include_timestamps (bool): Whether to include timestamp data
            
        Returns:
            pandas.DataFrame: Detailed experiment data
        """
        
        if experiment_id not in self.experiments:
            raise ValueError(f"Experiment {experiment_id} not found")
            
        exp = self.experiments[experiment_id]
        
        # Generate control group data
        control_converted = np.random.choice([0, 1], 
                                           size=exp['control']['visitors'],
                                           p=[1-exp['control']['conversion_rate'], 
                                              exp['control']['conversion_rate']])
        
        control_data = pd.DataFrame({
            'user_id': [f"ctrl_{i:06d}" for i in range(exp['control']['visitors'])],
            'variant': 'control',
            'converted': control_converted
        })
        
        # Generate test group data
        test_converted = np.random.choice([0, 1], 
                                        size=exp['test']['visitors'],
                                        p=[1-exp['test']['conversion_rate'], 
                                           exp['test']['conversion_rate']])
        
        test_data = pd.DataFrame({
            'user_id': [f"test_{i:06d}" for i in range(exp['test']['visitors'])],
            'variant': 'test',
            'converted': test_converted
        })
        
        # Combine data
        data = pd.concat([control_data, test_data], ignore_index=True)
        
        # Add timestamps if requested
        if include_timestamps:
            start_date = datetime.strptime(exp['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(exp['end_date'], '%Y-%m-%d')
            
            # Generate random timestamps between start and end date
            time_range = (end_date - start_date).total_seconds()
            random_seconds = np.random.uniform(0, time_range, len(data))
            timestamps = [start_date + timedelta(seconds=s) for s in random_seconds]
            
            data['timestamp'] = timestamps
            data['date'] = pd.to_datetime(data['timestamp']).dt.date
        
        # Add some demographic data for realism
        data['device_type'] = np.random.choice(['mobile', 'desktop', 'tablet'], 
                                             size=len(data), 
                                             p=[0.6, 0.35, 0.05])
        
        data['traffic_source'] = np.random.choice(['organic', 'paid', 'direct', 'social'], 
                                                size=len(data), 
                                                p=[0.4, 0.3, 0.2, 0.1])
        
        return data
    
    def save_to_csv(self, experiment_id, filename=None):
        """Save experiment data to CSV file"""
        if filename is None:
            filename = f"{experiment_id}_data.csv"
            
        data = self.generate_detailed_data(experiment_id)
        filepath = os.path.join(os.path.dirname(__file__), filename)
        data.to_csv(filepath, index=False)
        return filepath
    
    def get_continuous_metric_data(self, experiment_id='revenue_test'):
        """
        Generate sample data for continuous metrics (e.g., revenue, time spent)
        """
        
        # Generate revenue data
        np.random.seed(42)  # For reproducibility
        
        # Control group: average revenue $25, std $15
        control_revenue = np.random.normal(25, 15, 1000)
        control_revenue = np.maximum(control_revenue, 0)  # No negative revenue
        
        # Test group: average revenue $28, std $16 (slight improvement)
        test_revenue = np.random.normal(28, 16, 1000)
        test_revenue = np.maximum(test_revenue, 0)
        
        return {
            'control': control_revenue.tolist(),
            'test': test_revenue.tolist(),
            'metric_name': 'Revenue per User ($)',
            'experiment_name': 'Revenue Optimization Test'
        }

# Create a global instance
mock_db = MockABDatabase()

def get_sample_experiment(experiment_id=None):
    """Convenience function to get sample experiment data"""
    if experiment_id is None:
        experiment_id = 'checkout_button_color'
    return mock_db.get_experiment(experiment_id)

def list_available_experiments():
    """List all available sample experiments"""
    return mock_db.get_experiment_summary()
