###
# @Header: 
#
#       Some comments are marked `@Important` either because: 
#          1) I don't know how things work _exactly_ in this language.
#          2) I'm unsure how costly the `thing` is or could be.
#          3) I have a strong feeling it should be made differently but:
#             a) I have no idea how.
#             b) I don't care that much but enough to annotate it
#
#       Because this is python and that it should be a `minimal viable product` to be
#       `presented`, I care less about dependencies.
#       If it were only me I would reduce them to reach 0, if possible.
#       Although compromises must be made, we should probably keep an eye on how much stuff we
#       import/depend on.
###

# @Note: Provides the `swagger UI`
# @Note: Hidden dependency here, `fastapi` depends on `Starlette`
from fastapi import FastAPI, HTTPException

# @Important: Do we actually _need_ that ? Answer: `fastapi` does so we do.
from pydantic import Field     # @Note: https://docs.pydantic.dev/latest/concepts/fields/
from pydantic import BaseModel # @Note: https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage

from typing import List, Optional, Dict
from uuid import uuid4

###
# @Classes: -------------------------------------------------------------------#
###
class Comment(BaseModel):
    id       : str
    text     : str
    # @Note: user_id -> notation (-1, 0, 1)
    notations: Dict[str, int] = {}

class Feedback(BaseModel):
    id      : str
    note    : Optional[str] = None
    # @ToDo: Maybe should add some parameter to let people have different min/max values
    rating  : int = Field(ge=1, le=5)
    comments: List[Comment] = []

class FeedbackCreate(BaseModel):
    note  : Optional[str]
    rating: int

class CommentCreate(BaseModel):
    text: str

class Notation(BaseModel):
    value  : int = Field(..., ge=-1, le=1)
    user_id: str

###
# @Globals: -------------------------------------------------------------------#
###
# @Important: Attribute used by `uvicorn`, should this really be global ?
app = FastAPI()
# @Note: temporary storage, DB should be used 
g_fb_dict: Dict[str, Feedback] = {}

###
# @Functions: Utilities -------------------------------------------------------#
###
def uuid_str_get():
    # @Note: Apparently `uuid1()` is not safe and could leak you computer's address
    # some_uuid = uuid1() 
    # @Note: `uuid4()` is supposed to be random, so it is safe
    some_uuid = uuid4() 
    return str(some_uuid)

# @Important: Is there a macro system in python to avoid a function call here ?
def http_is_not_found(resource, detail = "Resource"):
    reason_str = detail + " not found";
    if not resource: raise HTTPException(status_code=404, detail = reason_str)

###
# @Functions: Get routes functions --------------------------------------------#
###
@app.get("/feedback", response_model=List[Feedback])
def feedback_list():
    return list(g_fb_dict.values())

# @Important: This function raises HTTPException
@app.get("/feedback/{feedback_id}", response_model=Feedback)
def feedback_get(feedback_id: str):
    feedback = g_fb_dict.get(feedback_id)
    http_is_not_found(feedback, "Feedback")
    return feedback

###
# @Functions: Post routes functions -------------------------------------------#
###

# @Important: Is there a max limit in the dictionary ? What is it ?
# @ToDo: Implement ring buffer for the feedback dict
@app.post("/feedback", response_model=Feedback)
def feedback_create(data: FeedbackCreate):
    fb_id            = uuid_str_get()
    feedback         = Feedback(id = fb_id, note = data.note, rating = data.rating)
    g_fb_dict[fb_id] = feedback
    return feedback

# @Important: This function raises HTTPException
@app.post("/feedback/{feedback_id}/comments", response_model=Comment)
def comment_add(feedback_id: str, data: CommentCreate):
    feedback = g_fb_dict.get(feedback_id)
    http_is_not_found(feedback, "Feedback")
    comment = Comment(id=uuid_str_get(), text=data.text)
    feedback.comments.append(comment)
    return comment

# @Important: This function raises HTTPException
@app.post("/feedback/{feedback_id}/comments/{comment_id}/notation")
def notation_add(feedback_id: str, comment_id: str, notation: Notation):
    feedback = g_fb_dict.get(feedback_id)
    http_is_not_found(feedback, "Feedback")

    comment = next((c for c in feedback.comments if c.id == comment_id), None)
    http_is_not_found(feedback, "Comment")

    comment.notations[notation.user_id] = notation.value
    return {"message": "Notation recorded"}

