class Student(object):
    
    def __init__(
        self,
        name: str,
        language: str,
        track: str,
        programmingLanguage: str,
        favouriteCourse: str,
    ) -> None:
        self.name = name
        self.language = language
        self.track = track
        self.programmingLanguage = programmingLanguage
        self.favouriteCourse = favouriteCourse
