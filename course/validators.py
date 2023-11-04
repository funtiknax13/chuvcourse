from rest_framework.exceptions import ValidationError


class AnswerValidator:

    def __call__(self, value):
        tmp_answer = dict(value).get('answer')
        tmp_question = dict(value).get('question')
        tmp_user = dict(value).get('user')
        # if tmp_value and not True:
        #     raise ValidationError('The answer does not exist')
