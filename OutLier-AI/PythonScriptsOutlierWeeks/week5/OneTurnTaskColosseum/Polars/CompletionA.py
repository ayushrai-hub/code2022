import polars as pl

df = pl.DataFrame(
    {
        "parameter_fields": [
            [
                "color", "gender", "sub_brand", "mrp", "main_size",
                "style_description", "fit", "category", "final_ssn",
                "sub_gender", "brand", "sleeves"
            ]
        ],
        "item_params": [
            {
                "fit": "RE06",
                "color": "NA",
                "gender": "ME",
                "category": "AP",
                "final_ssn": "AW23",
                "sub_brand": "NA",
                "sub_gender": "AD",
                "mrp": "2499",
                "brand": "FLM",
                "sleeves": "NA",
                "main_size": "36",
                "style_description": "5POCKETDENIM",
            }
        ],
    }
)

df = (
    df.with_columns(
        # build a dict that contains all wanted keys
        pl.struct(["parameter_fields", "item_params"]).map_elements(
            lambda s: {
                **s["item_params"],                         # existing keys
                **{k: "" for k in s["parameter_fields"]     # add the missing ones
                   if k not in s["item_params"]}
            }
        ).alias("item_params")    # overwrite / replace the old column
    )
)

print(df)
s