from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, TextAreaField, DateField, SubmitField, StringField
from wtforms.validators import InputRequired, NumberRange


class CommentForm(FlaskForm):
    """
    下拉列表：选择分数
    单选框：选择是否点名
    文字域：填写评论
    日期域：提交时间
    提交按钮：提交
    """
    score = SelectField(label='评分',
                        validators=[NumberRange(min=1, max=10, message=' * 请给老师一个评分')],
                        render_kw={'id': 'score'},
                        choices=[(-1, '请选择'), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                                 (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)],
                        coerce=int)
    whether_call_roll = RadioField(label='是否会点名',
                                   validators=[InputRequired(' * 请选择老师是否点名')],
                                   render_kw={'id': 'call_roll'},
                                   choices=[(1, '会'), (0, '不会')],
                                   coerce=int)
    comment = TextAreaField(render_kw={'id': 'comment_bar',
                                       'cols': 30, 'rows': 10,
                                       'placeholder': '关于这位老师，你想说点什么'})
    submit_date = DateField(render_kw={'id': 'submit_date'})
    submit = SubmitField(render_kw={'id': 'hidden_submit'})
