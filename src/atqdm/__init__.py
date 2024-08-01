from datetime import datetime, timedelta
import sys
from tqdm import tqdm as tqdm_original
from collections import OrderedDict
from numbers import Number


class APBar:
    def __init__(
        self, iterable, period: int = 10, sensitivity: int = 1, bar_width: int = 10
    ) -> None:
        """
        Class constructor
         - iterable
         - period: 10, time between updates in seconds
         - sensitivity: 1, minimum difference vs previous progress to show
         - bar_width: 10, width of the progress bar pseudographics
        """
        self.iter = iter(iterable)
        self.len = len(iterable)
        self.maxdigits = len(str(self.len)) * 2 + 3
        self.step = 0
        self.last = -1
        self.period = period
        self.sensitivity = sensitivity
        self.ptime = datetime.now()
        self.stime = datetime.now()
        self.prefix = ""
        self.postfix = ""
        self.width = bar_width

    def __len__(self):
        return self.len

    def __iter__(self):
        return self

    def barchart(self):
        """
        Method to create pseudographics bar
        """
        full = chr(0x2588)
        two = chr(0x2593)
        third = chr(0x2592)
        none = chr(0x2591)
        output = "["
        progress = self.step / self.len * self.width
        for i in range(self.width):
            if progress >= i + 1:
                output += full
            elif progress >= i + 0.66:
                output += two
            elif progress >= i + 0.33:
                output += third
            else:
                output += none
        output += "]"
        return output

    def set_description(self, desc=None, refresh=True):
        """
        Set/modify description of the progress bar.

        Parameters
        ----------
        desc  : str, optional
        refresh  : bool, ignored
        """
        self.prefix = desc + ": " if desc else ""

    def set_description_str(self, desc):
        """
        Method to set text preceding pseudographics bar
         - desc: string to show at next(!) iteration
        """
        self.prefix = desc

    def set_postfix(self, ordered_dict=None, refresh=True, **kwargs):
        """
        Set/modify postfix (additional stats)
        with automatic formatting based on datatype.

        Parameters
        ----------
        ordered_dict  : dict or OrderedDict, optional
        refresh  : bool, ignored
        kwargs  : dict, optional
        """
        # Sort in alphabetical order to be more deterministic
        postfix = OrderedDict([] if ordered_dict is None else ordered_dict)
        for key in sorted(kwargs.keys()):
            postfix[key] = kwargs[key]
        # Preprocess stats according to datatype
        for key in postfix.keys():
            # Number: limit the length of the string
            if isinstance(postfix[key], Number):
                postfix[key] = self.format_num(postfix[key])
            # Else for any other type, try to get the string conversion
            elif not isinstance(postfix[key], str):
                postfix[key] = str(postfix[key])
            # Else if it's a string, don't need to preprocess anything
        # Stitch together to get the final postfix
        self.postfix = ", ".join(
            key + "=" + postfix[key].strip() for key in postfix.keys()
        )

    def set_postfix_str(self, s):
        """
        Method to set text at the end of the string
         - s: string to show at next(!) iteration
        """
        self.postfix = "#" + str(s)

    def pp(
        self,
        percentage: int,
        timespent: timedelta = None,
        estimate: timedelta = None,
    ):
        """
        Pretty printing
         - percentage: progress in percents
         - timespent: time already spent
         - estimate: time left until the end
        """

        if timespent is None or estimate is None:
            time_string = ""
        else:
            if estimate.total_seconds() < 0:  # if out of boundaries end of loop
                es = "00:00:00"
            else:
                es = str(estimate).split(".")[0]
            ts = str(timespent).split(".")[0]
            time_string = f"{ts: >8}" + chr(0x25BA) + f"{es: >8}"
        percentage_string = f"{percentage:02d}%"
        digits_string = f"({self.step}/{self.len})"
        print(
            f"\n{datetime.now().strftime('%Y.%m.%d %H:%M:%S')}| {self.prefix}{self.barchart()}{percentage_string: <4} {digits_string: <{self.maxdigits}}{time_string}  {self.postfix} ",
            end="",
        )

    def __next__(self):
        self.step += 1
        ctime = datetime.now()
        delta_sec = (ctime - self.ptime).total_seconds()
        if self.last == -1:
            self.last = 0
            self.pp(0, None, None)
        elif delta_sec >= self.period or self.step == self.len:
            self.ptime = ctime
            progress = int(100 * self.step / self.len)
            timespent = ctime - self.stime
            totaltime = timespent / self.step * self.len
            estimate = totaltime - timespent
            if progress >= self.last + self.sensitivity:
                self.last = progress
                self.pp(
                    percentage=progress,
                    timespent=timespent,
                    estimate=estimate,
                )
            else:
                print(".", end="")
        if self.step > self.len:
            print("\n")
            raise StopIteration
        return next(self.iter)


def tqdm(iterable):
    """
    Function to create instance of a APBar class
    """
    try:
        if (
            "wandb" in sys.modules
            and hasattr(sys.modules["wandb"], "run")
            and sys.modules["wandb"].run is not None
        ) or (
            "comet_ml" in sys.modules
            and sys.modules["comet_ml"].get_running_experiment() is not None
        ):
            return APBar(iterable=iterable)
    except:
        pass
    return tqdm_original(iterable=iterable)


if __name__ == "__main__":
    pass
