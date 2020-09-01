from models import BoxesModel

class BoxesService:
  def __init__(self):
    self.model = BoxesModel()

  def create(self, params):
    self.model.create(params["text"], params["Description"], params["UserId"])