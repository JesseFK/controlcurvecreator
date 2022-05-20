import os
import sys
from maya import cmds


class ControllerTemplate:
    """ This class constructs a template for NURBS curve controllers.
    The '__init__' method simply constructs the path and the template
    file name.
    """
    def __init__(self):
        self.base_path = os.environ['MAYA_SCRIPT_PATH'].split(';')[2]
        self.path = self.base_path+'/controlcurvecreator/controllers/'
        self.template = '__templates__'

    def update_path(self):
        version = cmds.about(version=True)
        for path in os.environ['MAYA_SCRIPT_PATH'].split(';'):
            if 'Documents/maya/{0}/scripts'.format(version) in path :
                self.base_path = path
    
    def update_templates(self):
        """ This method will update all the template files (except for
        '__templates__'). It will create new files if previously they
        did not exist.
        """
        template_file = open(self.path + self.template + '.ma', 'r')
        lines = template_file.readlines()
        line_numbers = []
        for i in enumerate(lines):
            if 'transform' in i[1] and 'template' in i[1]:
                line_numbers.append(i[0])
            elif 'createNode lightLinker' in i[1]:
                line_numbers.append(i[0])

        names = []
        for i in line_numbers:
            line_split = lines[i].split(' ')
            name = line_split[-1].rstrip('";\n').lstrip('"')
            if 'lightLinker' in name:
                pass
            else:
                names.append(name)

        for i in enumerate(zip(line_numbers, names)):
            start = line_numbers[i[0]]
            if i[0] == len(line_numbers):
                break

            end = line_numbers[i[0]+1]
            open(self.path + i[1][1] + '.ma', 'w').close()
            new_file = open(self.path + i[1][1] + '.ma', 'w')
            new_file.writelines(lines[0])
            new_file.write('//Name: ' + str(i[1][1]) + '.ma\n')
            new_file.writelines(lines[2:5])
            new_file.writelines(lines[start:end])
            new_file.write('// End of ' + str(i[1][1]) + '.ma\n')
            new_file.close()

    def get_controller_templates(self):
        """ This method lists all the files in the directory with the
        exception of the '__templates__' file. It will then return that
        list.

        :return: List of the files that contain the NURBS controllers.
        """
        controllers = []
        directory = os.listdir(self.path.rstrip('/'))
        for template in directory:
            if self.template.rstrip('__') in template:
                pass
            else:
                controllers.append(template)

        return controllers

    # noinspection PyShadowingBuiltins
    def import_controller(self, type='square'):
        """
        :param type: Type is a string argument that will look for that
        controller in the files, if there's nothing that matches it
        does nothing.
        """
        control = []
        for name in os.listdir(self.path):
            if type in self.template:
                cmds.warning("Can't import default file")
                break
            if type in str(name):
                imp = cmds.file(self.path+name, i=True, rnn=True)
                control.append(imp)

        if len(control) < 2:
            return control[0]
        else:
            return control
