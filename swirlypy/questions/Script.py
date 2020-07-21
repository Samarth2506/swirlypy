from swirlypy.questions.Recording import RecordingQuestion
# from swirlypy.question import CategoryQuestion
from courses import import_course_path
import swirlypy.colors as colors
from importlib import import_module

class ScriptQuestion(RecordingQuestion):
    """Presents a list of options in random order to the user to select
a correct ansewr from."""

    _required_ = ['user_script', 'correct_script', 'test_cases']

    # def get_response(self, data={}):
    #     # Parse the options and shuffle them, for variety.
    #     # Loop until the user selects the correct answer.
    #     #Get location of scripts of interes


    def test_response(self, response, data={}):
        """Check the response in the simplest way possible."""
        import os

        moduleNames = 'courses'+ '.Python_Programming' + '.scripts.'
        #user_script = importlib.import_module(moduleNames+self.user_script)
        #print('something')
        # correct_script = importlib.import_module(moduleNames+self.correct_script+'.'+self.correct_script)
        # test_cases = importlib.import_module(moduleNames+self.test_cases)
        p, m = (moduleNames+self.correct_script+'.'+self.correct_script).rsplit('.', 1)
        
        mod = import_module(p)
        met = getattr(mod, m)

        path = os.path.join(str(import_course_path.get_path()), 'Python_Programming', 'scripts', self.user_script) 
        print(path)
        print(response)
        if 'x' in response['values']:
            print('inside loop')
            os.system("code " + path)
        
        x = input("Enter done when ready to submit")

        print(met())

        #print(correct_script())
        print('I am here')
        # return response == self.answer
        return True

    # def selftest(self, on_err, on_warn):
    #     if self.answer not in self.choices:
    #         on_err("answer \"%s\" not in available choices" % self.answer)
    #     if not self.test_response(self.answer):
    #         on_err("test_response fails with correct answer")

#     def yaml_hook(self):
#         """If `choices` is a string, split is on semicolon to form a
# list."""
#         if type(self.choices) == str:
#             self.choices = self.choices.split(";")
