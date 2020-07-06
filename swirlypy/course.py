import yaml
import swirlypy.slug
import swirlypy.lesson
import os
import tarfile
import tempfile

from swirlypy.errors import *
import swirlypy.colors as colors
from swirlypy.colors import color, colorize
import swirlypy.questions
from swirlypy.data import Data

class Course:
    """Course is a concrete representation of a collection of lessons
    in one coherent unit."""

    def __init__(self, course, lessons, author, version, coursedir,
            **kwargs):
        self.course = course
        self.lessonnames = lessons.split(";")
        self.author = author
        self.description = ""
        self.version = version
        self.coursedir = coursedir
        self.__dict__.update(kwargs)

        # If the course is packaged, unpack it to a temporary directory,
        # which will automatically clean itself up. If the course exists
        # only in memory, for some reason, the packaged attribute will
        # not be set.
        if hasattr(self, "packaged") and self.packaged:
            self._tempdir_ = tempfile.TemporaryDirectory()
            tarfile.open(self.coursedir).extractall(
                    path=self._tempdir_.name)

            self.rawdir = os.path.join(self._tempdir_.name, self.pkgname)
        else:
            self.rawdir = self.coursedir

    def print(self):
        """Prints a textual representation of the course, including
        name, author, and description, if available."""
        if len(self.description) > 0:
            print("%s by %s: %s" % (self.course, self.author,
                self.description))
        else:
            print("%s by %s" % (self.course, self.author))

    def menu(self):
        """Prints a menu containing all of the lessons in the course,
        along with their index."""
        print("\nPress Ctrl+D at any point to exit to the menu.")
        for index, lesson in enumerate(self.lessonnames):
            colors.print_option("%d: %s" % (index + 1, lesson))

    # XXX: Include a flag to have return status indicate whether
    # warnings were present.
    def validate(self):
        """Perform self-tests to ensure that the course can be executed
        safely."""

        # Keep track of whether there have been any fatal errors.
        errs = False

        # Define some convenience functions.
        def print_err(string):
            errs = True
            colors.print_err(string)

        def print_warn(string):
            colors.print_warn(string)


        # Error cases
        for field in [ "course", "lessonnames", "author" ]:
            if not hasattr(self, field):
                print_err("course.yaml has no '%s' attribute" %
                        field)

        # Warning cases
        for field in [ "description", "organization", "version", \
                "published" ]:
            if not hasattr(self, field):
                print_warn("course.yaml has no '%s' attribute" %
                        field)

        # For each lesson, try to run tests. If not present, print a
        # warning.
        for lesson_number in range(1, len(self.lessonnames) + 1):
            # Load the lesson, and carefully report any errors loading
            # it.
            try:
                l = self.load_lesson(lesson_number)
            except (FileNotFoundError, CouldNotLoadQuestionsException) as e:
                print_err("Could not load Lesson %d from file: '%s'" %
                        (lesson_number, e))
                continue

            # If the load failed in any way, abort here.
            if l == None:
                continue

            # Run validate on the lesson, if available, and pass it
            # out print functions.
            if hasattr(l, "validate"):
                l.validate(print_err, print_warn)
            else:
                print_warn("%s has no self-tests" %
                        self.lessonnames[lesson_number - 1])

        # Return whether there were any fatal errors.
        return not errs

    def execute(self,m, data):
        """Repeatedly prompts the user for lessons to run until
        explictly exited."""

        # Loop until user EOF.
        while True:
            # Present the menu.
            self.menu()
            try:
                colors.print_inst("Selection: ", end="")
                identifier = input().strip()
                self.execute_lesson(identifier, m,data)
            except NoSuchLessonException:
                colors.print_err("No lesson: %s" % identifier)
            except EOFError:
                # If the user hits CTRL-D, exit.
                # XXX: Tell the user this.
                print()
                print("Returning to main menu..")
                return

    def execute_lesson(self, identifier,m, data):
        """Executes a lesson based on a given identifier. This can be
        either an index (one-based) or a string matching a lesson name.
        If none can be found, it throws a NoSuchLessonException."""

        # Load the lesson, if possible.
        lesson = self.load_lesson(identifier)

        # If the "data" directory is present, load it up and pass it
        # along in the lesson data.
        if os.path.isdir(os.path.join(self.rawdir, "data")):
            provided = Data(os.path.join(self.rawdir, "data"))
        else:
            provided = None
        # print(data)
        # print(m)
        data.update({'m' : m})
        initial_data = data
        initial_data["coursedir"] = self.coursedir
        initial_data["rawdir"] = self.rawdir
        initial_data["provided"] = provided
        # Execute it.
        data = lesson.execute(initial_data)

        # Print a seperator to show it's complete.
        print()
        colors.print_exit("Lesson complete!")

    def load_lesson(self, identifier):
        """Loads a lesson from YAML based on a given identifier. This
        can be either an index (one-based) or a string matching a lesson
        name. If none can be found, it throws a
        NoSuchLessonException."""

        # Create an empty lesson name to refer to.
        lessonname = ""

        # Try to convert the identifier to an integer, failing silently
        # if it is not.
        try:
            identifier = int(identifier)
        except ValueError:
            pass

        # If it's an index, use it directly.
        if type(identifier) == int:
            try:
                lessonname = self.lessonnames[identifier - 1]
            except IndexError:
                raise NoSuchLessonException("Invalid lesson index")
        else:
            # If it's not an index, look it up, and then use the
            # resultant index.
            try:
                lessonname = self.lessonnames[
                        self.lessonnames.index(identifier)]
            except ValueError:
                raise NoSuchLessonException("Invalid lesson: %s" %
                        identifier)

        # We can construct the path that the lesson should be available
        # at by combining the course directory, "lessons", and the
        # slugified lesson name.
        lessonpath = os.path.join(self.rawdir, "lessons",
                swirlypy.slug.slugify(lessonname) + ".yaml")

        # Open the lesson and parse it from YAML.
        with open(lessonpath, "r") as f:
            lesson = swirlypy.lesson.Lesson.load_yaml(f)
        return lesson

    # XXX: Decide on and document the hardcoded course.yaml file here.
    @classmethod
    def load(cls, coursedir):
        """Loads a whole Course from the given course directory."""
        # Fill in a bit of metadata about the given path.
        pkgname = os.path.basename(coursedir).split(".")[0]
        # print(coursedir)
        # coursedir = "../" + coursedir
        packaged = os.path.isfile(coursedir)
        #print(packaged)
        # We have to have slightly different methods of opening the
        # right file depending on whether the course is packaged or
        # raw. We do this with an inline if statement - what else?
        with tarfile.open(coursedir).extractfile(os.path.join(
            pkgname, "course.yaml")) if packaged else \
                open(os.path.join(coursedir, "course.yaml"), "r") as f:
            course = cls.load_yaml(f, coursedir)

            # Fill in the previous metadata here.
            course.pkgname = pkgname
            course.packaged = packaged

            # If the course has supplementary question types, then load
            # them.
            extra_questionsdir = os.path.join(course.coursedir,
                    "questions")
            if os.path.isdir(extra_questionsdir):
                swirlypy.questions.load(extra_questionsdir)

            # Finally, return it.
            return course

    @classmethod
    def load_yaml(cls, file, coursedir):
        """Tries to construct a Course object from the first element in
        a given YAML file using yaml.safe_load. Dictionary keys are
        converted to lowercase."""
        # Load the YAML.
        y = yaml.safe_load(file)

        # Ensure that the first element exists. This should allow us to
        # safely access y[0].
        if len(y) < 1: raise NoCoursePresentException()

        # Lowercase all of the keys so that we can use it in the
        # constructor.
        document = dict((k.lower(), v) for k, v in y[0].items())

        # Construct a Course and return it.
        return cls(coursedir = coursedir, **document)
