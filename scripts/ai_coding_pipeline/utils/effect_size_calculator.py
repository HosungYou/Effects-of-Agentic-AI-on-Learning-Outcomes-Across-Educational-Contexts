#!/usr/bin/env python3
"""
Effect size calculation utilities.
Converts various statistics to Hedges' g with standard errors.
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class EffectSizeCalculator:
    """Calculate Hedges' g from various input statistics."""

    @staticmethod
    def cohens_d_to_hedges_g(d: float, n1: int, n2: int) -> Tuple[float, float]:
        """
        Convert Cohen's d to Hedges' g with small-sample correction.

        Args:
            d: Cohen's d value
            n1: Sample size group 1
            n2: Sample size group 2

        Returns:
            (hedges_g, standard_error)
        """
        # Small-sample correction factor (Hedges, 1981)
        df = n1 + n2 - 2
        j = 1 - (3 / (4 * df - 1))
        g = d * j

        # Standard error of g
        n_total = n1 + n2
        se_g = np.sqrt((n_total / (n1 * n2)) + (g**2 / (2 * n_total)))

        return g, se_g

    @staticmethod
    def means_to_hedges_g(m1: float, m2: float, sd1: float, sd2: float,
                         n1: int, n2: int) -> Tuple[float, float]:
        """
        Calculate Hedges' g from means and standard deviations.

        Args:
            m1: Mean of group 1 (treatment)
            m2: Mean of group 2 (control)
            sd1: SD of group 1
            sd2: SD of group 2
            n1: Sample size group 1
            n2: Sample size group 2

        Returns:
            (hedges_g, standard_error)
        """
        # Pooled standard deviation
        df1 = n1 - 1
        df2 = n2 - 1
        pooled_sd = np.sqrt(((df1 * sd1**2) + (df2 * sd2**2)) / (df1 + df2))

        # Cohen's d
        d = (m1 - m2) / pooled_sd

        # Convert to Hedges' g
        return EffectSizeCalculator.cohens_d_to_hedges_g(d, n1, n2)

    @staticmethod
    def prepost_to_hedges_g(m_pre: float, m_post: float, sd_pre: float,
                           sd_post: float, n: int, r: float = 0.5) -> Tuple[float, float]:
        """
        Calculate Hedges' g for pre-post design (within-subjects).

        Args:
            m_pre: Mean at pretest
            m_post: Mean at posttest
            sd_pre: SD at pretest
            sd_post: SD at posttest
            n: Sample size
            r: Correlation between pre and post (default: 0.5)

        Returns:
            (hedges_g, standard_error)
        """
        # Average SD
        sd_avg = (sd_pre + sd_post) / 2

        # Standardized mean difference
        d = (m_post - m_pre) / sd_avg

        # Correction factor for within-subjects
        df = n - 1
        j = 1 - (3 / (4 * df - 1))
        g = d * j

        # Standard error (accounting for correlation)
        se_g = np.sqrt((2 * (1 - r) / n) + (g**2 / (2 * n)))

        return g, se_g

    @staticmethod
    def t_to_hedges_g(t: float, n1: int, n2: int) -> Tuple[float, float]:
        """
        Convert t-statistic to Hedges' g.

        Args:
            t: t-statistic value
            n1: Sample size group 1
            n2: Sample size group 2

        Returns:
            (hedges_g, standard_error)
        """
        # Convert t to Cohen's d
        d = t * np.sqrt((n1 + n2) / (n1 * n2))

        # Convert to Hedges' g
        return EffectSizeCalculator.cohens_d_to_hedges_g(d, n1, n2)

    @staticmethod
    def f_to_hedges_g(f: float, n1: int, n2: int) -> Tuple[float, float]:
        """
        Convert F-statistic to Hedges' g (for two groups).

        Args:
            f: F-statistic value
            n1: Sample size group 1
            n2: Sample size group 2

        Returns:
            (hedges_g, standard_error)
        """
        # F = t^2 for two groups
        t = np.sqrt(f)

        return EffectSizeCalculator.t_to_hedges_g(t, n1, n2)

    @staticmethod
    def r_to_hedges_g(r: float, n: int) -> Tuple[float, float]:
        """
        Convert correlation to Hedges' g (approximate).

        Args:
            r: Correlation coefficient
            n: Total sample size

        Returns:
            (hedges_g, standard_error)

        Note: This assumes equal group sizes and dichotomous grouping variable.
        """
        # Convert r to d (assuming equal groups)
        d = (2 * r) / np.sqrt(1 - r**2)

        # Assume equal groups
        n1 = n2 = n // 2

        return EffectSizeCalculator.cohens_d_to_hedges_g(d, n1, n2)

    @staticmethod
    def hedges_g_variance(g: float, n1: int, n2: int) -> float:
        """
        Calculate variance of Hedges' g.

        Args:
            g: Hedges' g value
            n1: Sample size group 1
            n2: Sample size group 2

        Returns:
            Variance of g
        """
        n_total = n1 + n2
        var_g = (n_total / (n1 * n2)) + (g**2 / (2 * n_total))

        return var_g

    @staticmethod
    def validate_effect_size(g: float, se: float, n1: int, n2: int,
                            max_g: float = 5.0, min_n: int = 10) -> Dict[str, Any]:
        """
        Validate effect size for quality control.

        Args:
            g: Hedges' g value
            se: Standard error
            n1: Sample size group 1
            n2: Sample size group 2
            max_g: Maximum allowable |g|
            min_n: Minimum sample size per group

        Returns:
            Validation result dictionary
        """
        issues = []
        warnings = []

        # Check effect size magnitude
        if abs(g) > max_g:
            issues.append(f"Effect size |g| = {abs(g):.2f} exceeds maximum {max_g}")

        # Check sample sizes
        if n1 < min_n:
            issues.append(f"Group 1 sample size {n1} below minimum {min_n}")
        if n2 < min_n:
            issues.append(f"Group 2 sample size {n2} below minimum {min_n}")

        # Check for unreasonably small SE
        expected_min_se = np.sqrt(2 / (n1 + n2))
        if se < expected_min_se * 0.5:
            warnings.append(f"Standard error {se:.4f} unusually small")

        # Check for unreasonably large SE
        expected_max_se = np.sqrt(4 / min(n1, n2))
        if se > expected_max_se:
            warnings.append(f"Standard error {se:.4f} unusually large")

        # 95% confidence interval
        ci_lower = g - 1.96 * se
        ci_upper = g + 1.96 * se

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'g': g,
            'se': se,
            'ci_95': [ci_lower, ci_upper],
            'n1': n1,
            'n2': n2
        }

    @staticmethod
    def extract_effect_size(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intelligently extract effect size from various data formats.

        Args:
            data: Dictionary with effect size data in various formats

        Returns:
            Standardized effect size dictionary with g and se
        """
        result = {
            'g': None,
            'se': None,
            'method': None,
            'valid': False,
            'issues': []
        }

        try:
            # Case 1: Direct Hedges' g reported
            if 'hedges_g' in data and data['hedges_g'] is not None:
                g = float(data['hedges_g'])
                se = float(data.get('se_g', data.get('se', 0)))

                if se == 0 and 'n1' in data and 'n2' in data:
                    # Calculate SE if not provided
                    n1, n2 = int(data['n1']), int(data['n2'])
                    se = np.sqrt(EffectSizeCalculator.hedges_g_variance(g, n1, n2))

                result.update({'g': g, 'se': se, 'method': 'direct_hedges_g'})

            # Case 2: Cohen's d reported
            elif 'cohens_d' in data and data['cohens_d'] is not None:
                d = float(data['cohens_d'])
                n1, n2 = int(data['n1']), int(data['n2'])
                g, se = EffectSizeCalculator.cohens_d_to_hedges_g(d, n1, n2)
                result.update({'g': g, 'se': se, 'method': 'cohen_d_conversion'})

            # Case 3: Means and SDs
            elif all(k in data for k in ['m1', 'm2', 'sd1', 'sd2', 'n1', 'n2']):
                m1, m2 = float(data['m1']), float(data['m2'])
                sd1, sd2 = float(data['sd1']), float(data['sd2'])
                n1, n2 = int(data['n1']), int(data['n2'])
                g, se = EffectSizeCalculator.means_to_hedges_g(m1, m2, sd1, sd2, n1, n2)
                result.update({'g': g, 'se': se, 'method': 'means_sds'})

            # Case 4: Pre-post design
            elif all(k in data for k in ['m_pre', 'm_post', 'sd_pre', 'sd_post', 'n']):
                m_pre, m_post = float(data['m_pre']), float(data['m_post'])
                sd_pre, sd_post = float(data['sd_pre']), float(data['sd_post'])
                n = int(data['n'])
                r = float(data.get('r_prepost', 0.5))
                g, se = EffectSizeCalculator.prepost_to_hedges_g(
                    m_pre, m_post, sd_pre, sd_post, n, r
                )
                result.update({'g': g, 'se': se, 'method': 'prepost'})

            # Case 5: t-statistic
            elif 't' in data and 'n1' in data and 'n2' in data:
                t = float(data['t'])
                n1, n2 = int(data['n1']), int(data['n2'])
                g, se = EffectSizeCalculator.t_to_hedges_g(t, n1, n2)
                result.update({'g': g, 'se': se, 'method': 't_statistic'})

            # Case 6: F-statistic
            elif 'f' in data and 'n1' in data and 'n2' in data:
                f = float(data['f'])
                n1, n2 = int(data['n1']), int(data['n2'])
                g, se = EffectSizeCalculator.f_to_hedges_g(f, n1, n2)
                result.update({'g': g, 'se': se, 'method': 'f_statistic'})

            # Case 7: Correlation
            elif 'r' in data and 'n' in data:
                r = float(data['r'])
                n = int(data['n'])
                g, se = EffectSizeCalculator.r_to_hedges_g(r, n)
                result.update({'g': g, 'se': se, 'method': 'correlation'})

            else:
                result['issues'].append("No recognized effect size format found")
                return result

            # Validate
            if result['g'] is not None:
                n1 = data.get('n1', data.get('n', 0) // 2)
                n2 = data.get('n2', data.get('n', 0) // 2)
                validation = EffectSizeCalculator.validate_effect_size(
                    result['g'], result['se'], n1, n2
                )
                result.update(validation)

        except Exception as e:
            result['issues'].append(f"Extraction failed: {str(e)}")
            logger.error(f"Effect size extraction error: {e}")

        return result


def test_effect_size_calculator():
    """Test effect size calculator functionality."""
    print("Testing Effect Size Calculator...\n")

    calc = EffectSizeCalculator()

    # Test 1: Means to Hedges' g
    print("1. Testing means to Hedges' g:")
    g, se = calc.means_to_hedges_g(m1=85.5, m2=78.2, sd1=12.3, sd2=13.1, n1=50, n2=48)
    print(f"   g = {g:.3f}, SE = {se:.3f}")

    # Test 2: Cohen's d to Hedges' g
    print("\n2. Testing Cohen's d to Hedges' g:")
    g, se = calc.cohens_d_to_hedges_g(d=0.65, n1=30, n2=30)
    print(f"   g = {g:.3f}, SE = {se:.3f}")

    # Test 3: t to Hedges' g
    print("\n3. Testing t-statistic to Hedges' g:")
    g, se = calc.t_to_hedges_g(t=2.45, n1=35, n2=35)
    print(f"   g = {g:.3f}, SE = {se:.3f}")

    # Test 4: F to Hedges' g
    print("\n4. Testing F-statistic to Hedges' g:")
    g, se = calc.f_to_hedges_g(f=6.0, n1=40, n2=40)
    print(f"   g = {g:.3f}, SE = {se:.3f}")

    # Test 5: Pre-post to Hedges' g
    print("\n5. Testing pre-post to Hedges' g:")
    g, se = calc.prepost_to_hedges_g(
        m_pre=72.5, m_post=81.3, sd_pre=11.2, sd_post=10.8, n=45, r=0.6
    )
    print(f"   g = {g:.3f}, SE = {se:.3f}")

    # Test 6: Validation
    print("\n6. Testing validation:")
    validation = calc.validate_effect_size(g=0.55, se=0.22, n1=40, n2=40)
    print(f"   Valid: {validation['valid']}")
    print(f"   95% CI: [{validation['ci_95'][0]:.3f}, {validation['ci_95'][1]:.3f}]")

    # Test 7: Extract from various formats
    print("\n7. Testing intelligent extraction:")

    data1 = {'m1': 85, 'm2': 78, 'sd1': 12, 'sd2': 13, 'n1': 50, 'n2': 50}
    result1 = calc.extract_effect_size(data1)
    print(f"   From means: g = {result1['g']:.3f}, method = {result1['method']}")

    data2 = {'t': 2.5, 'n1': 35, 'n2': 35}
    result2 = calc.extract_effect_size(data2)
    print(f"   From t: g = {result2['g']:.3f}, method = {result2['method']}")

    print("\nAll tests completed!")


if __name__ == "__main__":
    test_effect_size_calculator()
