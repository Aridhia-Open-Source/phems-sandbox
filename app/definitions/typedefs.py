import pandas as pd

from typing import TypeAlias

TrainTestTuple: TypeAlias = tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]
