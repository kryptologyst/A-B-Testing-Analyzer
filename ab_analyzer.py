"""
A/B Testing Analyzer - Core Analysis Module
Provides statistical analysis for A/B testing experiments
"""

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.power import ttest_power
import warnings
warnings.filterwarnings('ignore')

class ABTestAnalyzer:
    """
    A comprehensive A/B testing analyzer that performs statistical tests
    and provides insights for conversion rate optimization.
    """
    
    def __init__(self):
        self.results = {}
        
    def analyze_proportions(self, control_conversions, control_visitors, 
                          test_conversions, test_visitors, alpha=0.05):
        """
        Analyze A/B test using two-proportion z-test
        
        Args:
            control_conversions (int): Number of conversions in control group
            control_visitors (int): Total visitors in control group
            test_conversions (int): Number of conversions in test group
            test_visitors (int): Total visitors in test group
            alpha (float): Significance level (default 0.05)
            
        Returns:
            dict: Analysis results including statistics and interpretation
        """
        
        # Input validation
        if any(val <= 0 for val in [control_visitors, test_visitors]):
            raise ValueError("Visitor counts must be positive")
        if control_conversions > control_visitors or test_conversions > test_visitors:
            raise ValueError("Conversions cannot exceed visitors")
        if not 0 < alpha < 1:
            raise ValueError("Alpha must be between 0 and 1")
            
        # Calculate conversion rates
        control_rate = control_conversions / control_visitors
        test_rate = test_conversions / test_visitors
        
        # Perform two-proportion z-test
        counts = [control_conversions, test_conversions]
        nobs = [control_visitors, test_visitors]
        
        z_stat, p_value = proportions_ztest(counts, nobs)
        
        # Calculate confidence interval for difference
        pooled_rate = sum(counts) / sum(nobs)
        se_diff = np.sqrt(pooled_rate * (1 - pooled_rate) * (1/nobs[0] + 1/nobs[1]))
        margin_error = stats.norm.ppf(1 - alpha/2) * se_diff
        diff = test_rate - control_rate
        ci_lower = diff - margin_error
        ci_upper = diff + margin_error
        
        # Calculate effect size (relative lift)
        relative_lift = ((test_rate - control_rate) / control_rate) * 100 if control_rate > 0 else 0
        
        # Statistical power calculation
        effect_size = abs(diff) / np.sqrt(pooled_rate * (1 - pooled_rate))
        power = ttest_power(effect_size, sum(nobs), alpha, alternative='two-sided')
        
        # Determine statistical significance
        is_significant = p_value < alpha
        
        # Create results dictionary
        results = {
            'control_rate': control_rate,
            'test_rate': test_rate,
            'difference': diff,
            'relative_lift_percent': relative_lift,
            'z_statistic': z_stat,
            'p_value': p_value,
            'alpha': alpha,
            'is_significant': is_significant,
            'confidence_interval': (ci_lower, ci_upper),
            'statistical_power': power,
            'sample_sizes': {'control': control_visitors, 'test': test_visitors},
            'conversions': {'control': control_conversions, 'test': test_conversions}
        }
        
        # Add interpretation
        if is_significant:
            if test_rate > control_rate:
                interpretation = f"Test variant performs significantly better than control (p={p_value:.4f})"
            else:
                interpretation = f"Test variant performs significantly worse than control (p={p_value:.4f})"
        else:
            interpretation = f"No significant difference between variants (p={p_value:.4f})"
            
        results['interpretation'] = interpretation
        
        self.results = results
        return results
    
    def analyze_continuous(self, control_values, test_values, alpha=0.05):
        """
        Analyze A/B test for continuous metrics using t-test
        
        Args:
            control_values (list): Values from control group
            test_values (list): Values from test group
            alpha (float): Significance level
            
        Returns:
            dict: Analysis results
        """
        
        control_values = np.array(control_values)
        test_values = np.array(test_values)
        
        # Perform t-test
        t_stat, p_value = stats.ttest_ind(control_values, test_values)
        
        # Calculate descriptive statistics
        control_mean = np.mean(control_values)
        test_mean = np.mean(test_values)
        control_std = np.std(control_values, ddof=1)
        test_std = np.std(test_values, ddof=1)
        
        # Effect size (Cohen's d)
        pooled_std = np.sqrt(((len(control_values) - 1) * control_std**2 + 
                             (len(test_values) - 1) * test_std**2) / 
                            (len(control_values) + len(test_values) - 2))
        cohens_d = (test_mean - control_mean) / pooled_std
        
        # Confidence interval for difference
        se_diff = np.sqrt(control_std**2/len(control_values) + test_std**2/len(test_values))
        df = len(control_values) + len(test_values) - 2
        t_critical = stats.t.ppf(1 - alpha/2, df)
        margin_error = t_critical * se_diff
        diff = test_mean - control_mean
        ci_lower = diff - margin_error
        ci_upper = diff + margin_error
        
        results = {
            'control_mean': control_mean,
            'test_mean': test_mean,
            'control_std': control_std,
            'test_std': test_std,
            'difference': diff,
            't_statistic': t_stat,
            'p_value': p_value,
            'alpha': alpha,
            'is_significant': p_value < alpha,
            'cohens_d': cohens_d,
            'confidence_interval': (ci_lower, ci_upper),
            'sample_sizes': {'control': len(control_values), 'test': len(test_values)}
        }
        
        # Add interpretation
        if results['is_significant']:
            if test_mean > control_mean:
                interpretation = f"Test group has significantly higher values than control (p={p_value:.4f})"
            else:
                interpretation = f"Test group has significantly lower values than control (p={p_value:.4f})"
        else:
            interpretation = f"No significant difference between groups (p={p_value:.4f})"
            
        results['interpretation'] = interpretation
        
        return results
    
    def sample_size_calculator(self, baseline_rate, minimum_detectable_effect, 
                             alpha=0.05, power=0.8):
        """
        Calculate required sample size for A/B test
        
        Args:
            baseline_rate (float): Expected conversion rate of control
            minimum_detectable_effect (float): Minimum effect size to detect (as decimal)
            alpha (float): Type I error rate
            power (float): Statistical power (1 - Type II error rate)
            
        Returns:
            dict: Sample size recommendations
        """
        
        # Calculate effect size
        test_rate = baseline_rate + minimum_detectable_effect
        pooled_rate = (baseline_rate + test_rate) / 2
        effect_size = abs(minimum_detectable_effect) / np.sqrt(pooled_rate * (1 - pooled_rate))
        
        # Calculate sample size using power analysis
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        
        n_per_group = ((z_alpha + z_beta)**2 * pooled_rate * (1 - pooled_rate)) / (minimum_detectable_effect**2)
        n_per_group = int(np.ceil(n_per_group))
        
        return {
            'sample_size_per_group': n_per_group,
            'total_sample_size': n_per_group * 2,
            'baseline_rate': baseline_rate,
            'test_rate': test_rate,
            'minimum_detectable_effect': minimum_detectable_effect,
            'alpha': alpha,
            'power': power,
            'effect_size': effect_size
        }
    
    def get_summary_report(self):
        """Generate a formatted summary report of the last analysis"""
        if not self.results:
            return "No analysis results available. Run an analysis first."
            
        report = f"""
A/B Test Analysis Summary
========================

Conversion Rates:
- Control: {self.results['control_rate']:.4f} ({self.results['control_rate']*100:.2f}%)
- Test: {self.results['test_rate']:.4f} ({self.results['test_rate']*100:.2f}%)
- Difference: {self.results['difference']:.4f} ({self.results['relative_lift_percent']:+.2f}%)

Statistical Results:
- Z-statistic: {self.results['z_statistic']:.4f}
- P-value: {self.results['p_value']:.4f}
- Significance Level: {self.results['alpha']:.3f}
- Statistical Power: {self.results['statistical_power']:.3f}

Confidence Interval (95%):
- Lower bound: {self.results['confidence_interval'][0]:.4f}
- Upper bound: {self.results['confidence_interval'][1]:.4f}

Sample Sizes:
- Control: {self.results['sample_sizes']['control']:,} visitors
- Test: {self.results['sample_sizes']['test']:,} visitors

Conclusion:
{self.results['interpretation']}
        """
        
        return report.strip()
