from dataclasses import dataclass

from src.exceptions import PageNumberError

@dataclass
class MatchesRequest:
    page_number: int
    player_name: str
    
    
    def __post_init__(self):
        try:
            int_page_number = int(self.page_number)
        except:
            raise PageNumberError("Номер страницы должен быть целым числом")
        if not int_page_number > 0:
            raise PageNumberError("Номер страницы должен быть целым числом")
        
        self.page_number = int_page_number

        