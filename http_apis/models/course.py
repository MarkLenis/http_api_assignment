class Course(object):

    def __init__(
        self,
        title: str,
        content: str,
        semester: int,
        pillar: str,
        tags: list[str] | None = None,
        tracks: list[str] | None = None,
        lecturers: list[str] | None = None,
        students: list[str] | None = None,
    ) -> None:
        self.title = title
        self.content = content
        self.semester = semester
        self.pillar = pillar
        self.tags = tags or []
        self.tracks = tracks or []
        self.lecturers = lecturers or []
        self.students = students or []
