import polars as pl
import json

def ensure_params_exist(row):
    """
    Ensure all parameter_fields exist in item_params with empty string if missing
    """
    parameter_fields = row['parameter_fields']
    item_params = row['item_params'].copy()  # Create a copy to avoid modifying original
    
    # Check each field in parameter_fields
    for field in parameter_fields:
        if field not in item_params:
            item_params[field] = ""  # Add missing field with empty string
    
    return item_params

# Apply the function to your DataFrame
df = df.with_columns(
    pl.struct(['parameter_fields', 'item_params'])
    .map_elements(
        lambda x: ensure_params_exist(x), 
        return_dtype=pl.Object
    )
    .alias('item_params')
)
