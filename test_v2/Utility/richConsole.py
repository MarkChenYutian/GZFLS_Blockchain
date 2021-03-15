from rich.console import Console

class console:
    c = Console()

    @classmethod
    def warning(cls, msg):
        cls.c.log("[yellow]WARNING[/yellow]  " + msg, _stack_offset=2)

    @classmethod
    def error(cls, msg):
        cls.c.log("[red]ERROR[/red]    " + msg, _stack_offset=2)

    @classmethod
    def info(cls, msg):
        cls.c.log("[blue]INFO[/blue]     " + msg, _stack_offset=2)
