from enum import Enum
import QuantLib as ql

class OptionType(Enum):
    Call = 1
    Put = 0

    @staticmethod
    def ql_type(option_type):
        if option_type == OptionType.Call:
            return ql.Option.Call
        elif option_type == OptionType.Put:
            return ql.Option.Put