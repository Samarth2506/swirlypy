import swirlypy.question

class Lesson:
    def __init__(self, questions, **kwargs):
        self.questions = questions
        self.__dict__.update(kwargs)

    def execute(self, initial_data = {}):
        """Executes all questions in sequence, storing data passed back
        by each of them, and passing it into the subsequent question.
        The merged data will be passed back as a return value."""

        # Declare a new variable to use to store any data that the
        # questions pass back, as well as any passed in initially.
        data = initial_data.copy()
        for question in self.questions:
            # Execute the questions in sequence, and pass each of them
            # the current data. If they return anything new, update the
            # data with it.
            new_data = question.execute(data=data)
            if type(new_data) == dict:
                data.update(new_data)

        # Return the data, with whatever updates have been applied.
        return data

    def validate(self, on_err, on_warn):
        for index, question in enumerate(self.questions):
            # Wrap on_err and on_warn with an index number.
            def question_on_err(string):
                on_err("%s at index %d: %s" % (
                    type(question).__name__, index, string))

            def question_on_warn(string):
                on_warn("%s at index %d: %s" % (
                    type(question).__name__, index, string))

            if hasattr(question, "basic_selftest"):
                question.basic_selftest(question_on_err,
                        question_on_warn)
            else:
                question_on_warn("no basic self tests")

            if hasattr(question, "selftest"):
                question.selftest(question_on_err, question_on_warn)
            else:
                question_on_warn("no self tests")

    @classmethod
    def load_yaml(cls, file):
        """Loads questions from the given YAML file using
        Question.load_yaml, and constructs an instance of this class
        using them."""
        questions = swirlypy.question.Question.load_yaml(file)
        return cls(questions)
