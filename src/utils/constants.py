"""
Application Constants
"""

# Feature columns
FEATURE_COLUMNS = [
    'age', 'sex', 'antibodies', 'anti_hvc', 'fibrosis', 'cirrhosis', 
    'alt', 'ast', 'albumin', 'platelets'
]

# Target column
TARGET_COLUMN = 'target'

# Model parameters
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5
