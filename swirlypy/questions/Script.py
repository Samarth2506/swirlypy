from swirlypy.questions.Recording import RecordingQuestion
# from swirlypy.question import CategoryQuestion
from courses import import_course_path
import swirlypy.colors as colors
from importlib import import_module
import importlib

class ScriptQuestion(RecordingQuestion):
    """Presents a list of options in random order to the user to select
a correct ansewr from."""

    _required_ = ['user_script', 'correct_script', 'test_cases']

    def test_response(self, response, data={}):
        """Check the response in the simplest way possible."""
        import os
        course = 'Demo_Course'
        # Import user and correct scripts as Python modules
        moduleNames = 'courses'+ '.' + course + '.scripts.'
    
        correct_mod, correct_func = (moduleNames+self.correct_script+'.'+self.correct_script).rsplit('.', 1)
        correct_import = import_module(correct_mod)
        correct_run = getattr(correct_import, correct_func) 
           
        # Open the user script with VS Code
        user_path = os.path.join(str(import_course_path.get_path()), course, 'scripts', self.user_script+'.py') 
        if 'open' in response['values']:
            colors.print_exit('Opening your script now.. \n')
            os.system("code " + user_path)
        
        # Prompt needed to acknowledge user is done coding
        x = input("Enter done when ready to submit: \n")

        #Load user script module
        user_mod, user_func = (moduleNames+self.user_script+'.'+ self.user_script).rsplit('.', 1)
        user_import = import_module(user_mod)
        user_run = getattr(user_import, user_func)
        
        # Reload module to update user response in script
        importlib.reload(user_import)
        user_run = getattr(user_import, user_func)
        
        # Show user what output is expected and the output of their script
        print("Output of your script: ", user_run())
        print("Expected output: ",correct_run())

        return user_run() == correct_run()

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
