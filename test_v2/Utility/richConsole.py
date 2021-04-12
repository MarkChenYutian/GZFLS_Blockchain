from rich.console import Console


class console:
    c = Console()
    dataPath = "./RuntimeLog.txt"

    @classmethod
    def initialize(cls):
        with open(cls.dataPath, "w") as f: f.write("")
        cls.info("Log File at {} cleared.".format(cls.dataPath))

    @classmethod
    def warning(cls, msg):
        with open(cls.dataPath, "a") as f:
            f.write("[WARNING]  " + msg + "\n")
        cls.c.log("\r[yellow]WARNING[/yellow]  " + msg, _stack_offset=2)

    @classmethod
    def error(cls, msg):
        with open(cls.dataPath, "a") as f:
            f.write("[ERROR]   " + msg + "\n")

        cls.c.log("\r[red]ERROR[/red]    " + msg, _stack_offset=2)

    @classmethod
    def info(cls, msg):
        with open(cls.dataPath, "a") as f:
            f.write("[INFO]    " + msg + "\n")

        # the below line is disabled such that info level log won't be printed to the console.
        cls.c.log("\r[blue]INFO[/blue]     " + msg, _stack_offset=2)
