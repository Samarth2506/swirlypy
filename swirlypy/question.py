#/usr/bin/python3
#
# This is another test of question classes.

import abc, yaml
from code import InteractiveConsole
from swirlypy.dictdiffer import DictDiffer
from swirlypy.errors import *
import swirlypy.colors as colors

# XXX: Add a __str__ method to represent the question in some way.
# XXX: Add some 'hint' capacity
# XXX: Provide an inbuilt capability to print errors or respond to
# incorrect user input.
class Question(object):
    """Question is an abstract class used to provide utilities for and
    embody a generic question to be asked in a course, which provides a
    prompt, or just text, request user response, and test it for
    correctness."""

    # Mark this class as an abstract.
    __metaclass__ = abc.ABCMeta

    _required_ = None

    def __init__(self, category, output, **kwargs):
        """Tries to construct the most specific possible Question
        subclass based on the given category. It will never construct an
        actual Question - instead, a CategoryQuestion. If the category
        is unavailable, it will raise an
        UnknownQuestionCategoryException."""

        ## Hold on tight. This is going to get really weird.

        # Make sure that we have the plugin questions module. We can't
        # import this earlier due to circular dependencies, but Python
        # will handle multiple imports for us sanely.
        import swirlypy.questions

        # Now we're going to try to create a dummy CategoryQuestion from
        # the plugins.
        qname = (category + "question").lower()
        if qname in swirlypy.questions.categories:
            # Here's it being created.
            dummy = swirlypy.questions.categories[qname](category,
                    output, **kwargs)
        else:
            raise UnknownQuestionCategoryException(qname)

        # Wait, dummy CategoryQuestion? Yeah. We're going to take all of
        # its fields and assign them to self.
        self.__dict__ = dummy.__dict__

        # Wait, WHAT? It's okay. We're almost done. All we have to do is
        # just go ahead and change self's class.
        self.__class__ = dummy.__class__

        # And call require
        self.require(self._required_)

        # Yeah. So it turns out that there's a fairly good reason for
        # all this. Python won't let you return from a constructor.
        # That's alright, I guess, but it also won't let you completely
        # reassign self to something different, like an instance of
        # another class. But you can change the __class__, and
        # therefore all the bound methods, and as long as we also copy
        # the fields, no one's any wiser that we used the wrong
        # constructor.

    # Require that the given list of fields is present in the object's
    # dictionary. If any are not, a MissingFieldException is raised.
    def require(self, fields):
        # If only one field is given, treat it sanely by wrapping it in
        # a list.
        if fields == None: return True
        elif type(fields) != list: fields = [fields]

        for field in fields:
            if not hasattr(self, field):
                raise MissingFieldException(field)

        return True

    # Output in whatever format desired, defaults to self.output.
    # XXX: Could be much more advanced; automatically paginating, for
    # example.
    def print(self):
        colors.print_question(self.output)

    @abc.abstractmethod
    def get_response(self, data={}):
        """Get user question response and returns it as an object that
        can be tested via test_response."""

    @abc.abstractmethod
    def test_response(self, response, data={}):
        """Test the user's response as returned by get_response,
        returning True if successful, and False if not."""

    def execute(self, data={}):
        """Execute the question in the default way, by first printing
        itself, then asking for a response and testing it in a loop
        until it is correct."""
        # XXX: Collect statistics here so that it can be used for
        # grading.

        # Print the output.
        self.print()

        # Loop until correct.
        while True:
            # Get the user's response.
            resp = self.get_response(data=data)

            # Test it. If correct (True), then break from this loop. If
            # not, print the hint, if it's present.
            testresult = self.test_response(resp, data=data)
            if testresult == True:
                break
            elif testresult == False:
                try:
                    colors.print_help(self.hint)
                except AttributeError:
                    pass
            else:
               # If the test is not a boolean, (i.e. None), then it was
               # not testable or relevant, for some reason.
               continue

    @classmethod
    def load_yaml(cls, file):
        """Tries to construct any number of Questions in the given YAML
        file by using yaml.safe_load. Dictionary keys are converted to
        lowercase."""
        # Try to load the YAML, minimizing code execution
        # vulnerabilities.
        y = yaml.safe_load(file)

        # Instantiate a list in which to return questions.
        questions = []

        for idx, document in enumerate(y):
            # First, lowercase keys in the given document.
            document = dict((k.lower(), v) for k, v in document.items())

            # Try to construct a class from the result (as **kwargs).
            # The __init__ method *should* ensure that the required
            # fields are present.

            try:
                question = cls(method="yaml", **document)
            except Exception as e:
                raise CouldNotLoadQuestionsException("Could not load Question %d \
in %s: %s" % (idx, file.name, e))

            questions.append(cls(method="yaml", **document))


        return questions

    @classmethod
    def doc(cls):
        def attrelseundoc(obj, string):
            """Returns the attribute represented by the object and
            string, unless it is in None, in which case it is replaced
            by "undocumented"."""
            attr = None
            if hasattr(obj, string):
                attr = getattr(obj, string)

            return attr if attr != None else "undocumented"

        # Find a list of all attributes containing "_hook" of the class.
        hookpairs = [(key, val) for key, val in cls.__dict__.items() \
                    if "_hook" in key]

        # Format the hook documentation nicely, if available.
        hookdocs = "\n".join(("  %s: %s" % (name, attrelseundoc(hook,
            "__doc__")) for name, hook in hookpairs))

        required = ', '.join(cls._required_) if \
                hasattr(cls, "required") else None

        docs = attrelseundoc(cls, "__doc__")

        return "%s\n\nRequired: %s\n\nHooks:\n%s" % (docs, required, \
                hookdocs)

    @classmethod
    def basic_selftest(cls, on_err, on_warn):
        def present_value(obj, string):
            """Return whether the given object's field is both present
and a value other than None or empty string."""
            attr = None
            if hasattr(obj, string): attr = getattr(obj, string)
            return not (attr == None or \
                    (type(attr) == str and attr == ""))

        if not present_value(cls, "__doc__"):
            on_warn("not documented")

        if not present_value(cls, "_required_"):
            on_warn("requirements not defined")

        hookpairs = ((key, val) for key, val in cls.__dict__.items() \
                if "_hook" in key)

        for hookname, hook in hookpairs:
            if not present_value(hook, "__doc__"):
                on_warn("%s not documented" % hookname)

class CategoryQuestion(Question):
    """CategoryQuestion is another abstract class that includes some of
    the boilerplate necessary to build safe questions that behave
    sanely, but have all of the convenience of Questions. Primarily,
    questions that inherit from CategoryQuestion do not have to override
    __init__."""

    # Mark this class as an abstract.
    __metaclass__ = abc.ABCMeta

    def __init__(self, category, output, method=None, **kwargs):
        self.category = category
        self.output = output
        self.__dict__.update(kwargs)

        # If present, run any hooks associated with the method. For
        # example, patching up YAML.
        if hasattr(self, "%s_hook" % method):
            getattr(self, "%s_hook" % method)()

    def yaml_hook(self):
        """Invoked after class instantiation, if the instantiation
        method is 'yaml'. Can be overridden to implement per-question
        type corrections from YAML."""
        pass

# XXX: Add a simpler way to drop out of the shell than asking the user
# to exit.
class ShellQuestion(CategoryQuestion):
    """ShellQuestion is a question template that handles most of the
    boilerplate necessary for asking questions that drop to a shell
    prompt."""

    bannerinfo = "Press CTRL-D to submit."

    # Mark this class as an abstract.
    __metaclass__ = abc.ABCMeta

    def shell(self, locals={}, newlocals={}):
        """Open a prompt with the given local variables. This could, for
        example, open a shell with a pristine copy of the question
        environment, or one with past input from the user, or load more
        data. Returns a DictDiffer which represents items the user
        changed."""

        # First, copy the locals to avoid disturbing the given dict, and
        # then add the given newlocals.
        ourlocals = locals.copy()
        ourlocals.update(newlocals)

        # Start a fresh console object. If we want to maintain state
        # between multiple shell() calls, we'll have to store the
        # locals.
        console = self.new_console(ourlocals)

        # Interact with the console until exiting. The bannerinfo will
        # be printed prior to the prompt.
        console.interact(banner=self.bannerinfo)

        # Retrieve the user's environment, and construct a DictDiffer
        # with it.
        return DictDiffer(console.locals, ourlocals)

    def new_console(self, locals):
        """Creates and returns a new interactive console that implements
        the same interfaces as code.InteractiveConsole. Locals are
        copied before modification."""
        return InteractiveConsole(locals.copy())
