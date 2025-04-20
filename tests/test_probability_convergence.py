import unittest
import numpy as np
from math import comb
import sys
import os

# Add parent directory to path to import from probability_convergence.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probability_convergence import theoretical_probability, theoretical_convergence

class TestProbabilityConvergence(unittest.TestCase):
    def test_theoretical_convergence(self):
        """Test that standard deviation convergence matches theoretical values."""
        test_ns = [2, 4, 10, 20, 50, 100]
        for n in test_ns:
            expected = 1 / (2 * np.sqrt(n))
            actual = theoretical_convergence(n)
            # Allow 1% tolerance
            self.assertAlmostEqual(actual, expected, delta=expected*0.01,
                                 msg=f"Failed for n={n}")

    def test_theoretical_probability(self):
        """Test that exact 50% probability matches theoretical values."""
        # Test cases with known values
        test_cases = [
            (2, 0.5),  # 2 flips: P(1 head) = 2C1 * (1/2)^2 = 0.5
            (4, 0.375),  # 4 flips: P(2 heads) = 4C2 * (1/2)^4 = 0.375
            (6, 0.3125)  # 6 flips: P(3 heads) = 6C3 * (1/2)^6 = 0.3125
        ]
        
        for n, expected in test_cases:
            actual = theoretical_probability(n)
            # Allow 0.1% tolerance
            self.assertAlmostEqual(actual, expected, delta=expected*0.001,
                                 msg=f"Failed for n={n}")

    def test_odd_flips_zero_probability(self):
        """Test that odd numbers of flips return zero probability."""
        odd_ns = [1, 3, 5, 7, 9]
        for n in odd_ns:
            self.assertEqual(theoretical_probability(n), 0,
                           f"Expected 0 probability for odd n={n}")

    def test_large_n_convergence(self):
        """Test that probability approaches zero for large n."""
        large_ns = [50, 100, 200]
        prev_prob = 1.0
        for n in large_ns:
            curr_prob = theoretical_probability(n)
            self.assertLess(curr_prob, prev_prob,
                          f"Probability should decrease for n={n}")
            prev_prob = curr_prob

if __name__ == '__main__':
    unittest.main() 