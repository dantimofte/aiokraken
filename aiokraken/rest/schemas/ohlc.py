import marshmallow.validate
import typing
import pandas as pd
import numpy as np
from marshmallow_dataframe import SplitDataFrameSchema

ohlc_df = pd.DataFrame(
    # Need some sample data to get proper dtypes...
    [[1567039620, '8746.4', '8751.5', '8745.7', '8745.7', '8749.3', '0.09663298', 8],
     [1567039680, '8745.7', '8747.3', '8745.7', '8747.3', '8747.3', '0.00929540', 1]],
    # grab that from kraken documentation
    columns=["time", "open", "high", "low", "close", "vwap", "volume", "count"]
)

# TODO : manage errors with : https://marshmallow.readthedocs.io/en/stable/extending.html#custom-class-meta-options ???

# {'error': [], 'result': {'XXBTZEUR': [[1567039620, '8746.4', '8751.5', '8745.7', '8745.7', '8749.3', '0.09663298', 8],
#                                       [1567039680, '8745.7', '8747.3', '8745.7', '8747.3', '8747.3', '0.00929540', 1],
#                                       [1567039740, '8747.3', '8748.0', '8747.3', '8748.0', '8748.0', '0.62570000', 3],
#                                       [1567039800, '8748.0', '8748.0', '8746.6', '8746.6', '8747.0', '0.04330887', 6],
#                                       [1567039860, '8746.6', '8751.4', '8746.6', '8748.5', '8748.1', '0.03098298', 4],
#                                       [1567039920, '8748.5', '8751.7', '8748.5', '8751.7', '8751.6', '0.10450040', 4],
#                                       [1567039980, '8751.7', '8751.7', '8751.6', '8751.6', '8751.6', '0.06860664', 5],
#                                       [1567040040, '8751.6', '8751.7', '8751.6', '8751.7', '8751.7', '0.23259337', 6],
#                                       [1567040100, '8751.7', '8753.1', '8751.7', '8753.1', '8752.2', '0.01496395', 3],
#                                       [1567040160, '8753.1', '8753.1', '8750.7', '8750.7', '8750.7', '1.26223001', 7],
#                                       [1567040220, '8750.7', '8750.7', '8746.7', '8746.7', '8747.2', '0.01844025', 3],
#                                       [1567040280, '8746.7', '8748.4', '8745.7', '8748.0', '8746.7', '0.27772793', 8],
#                                       [1567040340, '8748.0', '8749.2', '8748.0', '8749.2', '8749.2', '0.00750471', 1],
#                                       [1567040400, '8749.2', '8750.0', '8749.1', '8749.1', '8749.3', '0.01155843', 2],
#                                       [1567040460, '8749.1', '8749.9', '8749.1', '8749.8', '8749.8', '0.12814092', 4],
#                                       [1567040520, '8749.8', '8749.9', '8749.8', '8749.9', '8749.9', '0.13842572', 4],
#                                       [1567040580, '8749.9', '8749.9', '8749.9', '8749.9', '8749.9', '0.17761378', 4],
#                                       [1567040640, '8749.9', '8749.9', '8749.9', '8749.9', '8749.9', '0.03434231', 3],
#                                       [1567040700, '8749.9', '8749.9', '8749.7', '8749.7', '8749.7', '0.11389542', 4],
#                                       [1567040760, '8749.7', '8749.7', '8740.3', '8740.3', '8745.1', '0.41453152', 5],
#                                       [1567040820, '8740.3', '8740.3', '8735.6', '8739.1', '8736.2', '0.73934210', 4],
#                                       [1567040880, '8739.1', '8743.8', '8739.1', '8739.2', '8742.1', '0.59250003', 6],
#                                       [1567040940, '8739.2', '8745.8', '8739.2', '8745.7', '8745.7', '0.05624324', 5],
#                                       [1567041000, '8745.7', '8749.7', '8745.7', '8749.7', '8748.0', '0.22351499', 9],
#                                       [1567041060, '8749.7', '8749.7', '8746.1', '8746.7', '8746.9', '0.13758985', 6],
#                                       [1567041120, '8746.7', '8747.3', '8746.7', '8747.2', '8747.2', '0.00400000', 2],
#                                       [1567041180, '8747.2', '8749.8', '8746.7', '8746.7', '8747.5', '0.01437414', 3],
#                                       [1567041240, '8746.7', '8748.5', '8745.8', '8747.1', '8748.4', '0.79927987', 9],
#                                       [1567041300, '8747.1', '8750.0', '8747.1', '8750.0', '8749.2', '0.03725853', 3],
#                                       [1567041360, '8748.2', '8750.0', '8748.2', '8750.0', '8749.8', '1.21022828', 7],
#                                       [1567041420, '8750.0', '8750.0', '8750.0', '8750.0', '8750.0', '0.00500000', 1],
#                                       [1567041480, '8750.0', '8750.0', '8750.0', '8750.0', '8750.0', '0.03527364', 3],
#                                       [1567041540, '8750.0', '8750.0', '8750.0', '8750.0', '8750.0', '1.31659484', 3],
#                                       [1567041600, '8750.0', '8750.0', '8749.9', '8750.0', '8749.9', '1.11347357', 5],
#                                       [1567041660, '8750.0', '8750.0', '8750.0', '8750.0', '8750.0', '0.35528700', 4],
#                                       [1567041720, '8750.0', '8755.8', '8749.9', '8755.7', '8754.0', '3.98795136', 27],
#                                       [1567041780, '8755.7', '8755.7', '8753.7', '8755.7', '8755.3', '0.02876177', 3],
#                                       [1567041840, '8755.7', '8758.0', '8755.7', '8758.0', '8758.0', '0.02178000', 2],
#                                       [1567041900, '8758.0', '8758.0', '8758.0', '8758.0', '8758.0', '0.17849448', 3],
#                                       [1567041960, '8758.0', '8758.0', '8757.9', '8758.0', '8757.9', '0.01496327', 3],
#                                       [1567042020, '8758.0', '8758.0', '8758.0', '8758.0', '8758.0', '0.00641000', 1],
#                                       [1567042080, '8758.0', '8758.0', '8758.0', '8758.0', '8758.0', '0.29430485', 4],


# Ref : https://stackoverflow.com/questions/42231334/define-fields-programmatically-in-marshmallow-schema

class OHLCDataFrameSchema(SplitDataFrameSchema):
    """Automatically generated schema for ohlc dataframe"""

    class Meta:
        dtypes = ohlc_df.dtypes

    @marshmallow.pre_load(pass_many=False)
    def add_implicit(self, data, **kwargs):
        pass
        return {
            "data": data,
            "columns": ohlc_df.columns,
            "index": range(len(data)),
        }

    # load or dump ?
    # @marshmallow.post_load(pass_many=False)
    # def make_ohlc(self, data, **kwargs):
    #     return data  # TODO : embed in a specific type. all dataframes are not equivalent...


# # TODO : proper typing to limit ( and check ) pair name
# def pair_field_nested(name, schema):
#     return type(name + '_' + str(schema), (schema,), {
#         name: schema
#     })
#
#
# XXBTZEUR_OHLCDataFrameSchema = pair_field_nested('XXBTZEUR', OHLCDataFrameSchema)


# TMP to get it right...
class XXBTZEUR_OHLCDataFrameSchema(marshmallow.Schema):

    XXBTZEUR = marshmallow.fields.Nested(OHLCDataFrameSchema)

    # @marshmallow.pre_load(pass_many=False)
    # def add_implicit(self, data, **kwargs):
    #     return {
    #         "data": data,
    #         "columns": ohlc_df.columns,
    #         "index": [0],
    #     }