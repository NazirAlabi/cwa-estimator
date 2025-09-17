
class Course():
    def __init__(self, name, score, credits):
        self.name=name.lower().title()
        self.score=int(score)
        self.credits=int(credits)
    
    def __str__(self):
        return f"Course name: {self.name}, Estimated score: {self.score}, Credit hours: {self.credits} \n"