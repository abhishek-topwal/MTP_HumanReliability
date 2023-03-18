from PySide2 import QtWidgets, QtCore, QtGui
from datetime import datetime
from Helpers import WTrack
from Helpers.Translator import translate as _
import pygame


file = open("track_log.txt", "r+")
file.seek(0)
file.truncate()
dash_flag = 0
class Task(QtWidgets.QWidget):

    def __init__(self, parent):
        super(Task, self).__init__(parent)

        self.my_joystick = None

        # TRACK PARAMETERS ###
        self.parameters = {
            'taskplacement': 'topmid',
            'taskupdatetime': 20,
            'title': 'Tracking',
            'cursorcolor': '#0000FF',
            'cursorcoloroutside': '#e82610', #changes the outside color to red
            'automaticsolver': False,
            'displayautomationstate': True,
            'assistedsolver': False,
            'targetradius': 0.1,
            'joystickforce': 1.0,
            'cutofffrequency': 0.06,
            'equalproportions': True,
            'resetperformance': None,
            'coordinates':(0,0)
        }

        self.performance = {
            'total' : {'time_in_ms':0, 'time_out_ms':0, 'points_number':0, 'deviation_mean':0},
            'last'  : {'time_in_ms':0, 'time_out_ms':0, 'points_number':0, 'deviation_mean':0}
        }

        # Potentially translate task title
        self.parameters['title'] = _(self.parameters['title'])


    def onStart(self):

        # Define a QLabel object to potentially display automation mode
        self.modeFont = QtGui.QFont("sans-serif", int(self.height() / 35.), QtGui.QFont.Bold)
        self.modeLabel = QtWidgets.QLabel(self)
        self.modeLabel.setGeometry(QtCore.QRect(0.60 * self.width(), 0.60 * self.height(), 0.40 * self.width(), 0.40 * self.height()))
        self.modeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.modeLabel.setFont(self.modeFont)

        self.parameters['displaytitle'] = True

        # Set a WTrack Qt object
        self.widget = WTrack.WTrack(self, self.parameters['equalproportions'])

        # Create a layout for the widget
        layout = QtWidgets.QGridLayout()

        # Add the WTrack object to the layout
        layout.addWidget(self.widget)
        self.setLayout(layout)

        ############################ FOR JOYSTICK ############################################
        # pygame.joystick.init()

        # # Check for a joystick device
        # if pygame.joystick.get_count() == 0:
        #     self.parent().showCriticalMessage(
        #         _("Please plug a joystick for the '%s' task!") % (self.parameters['title']))
        # else:
        #     self.my_joystick = pygame.joystick.Joystick(0)
        #     self.my_joystick.init()
        #######################################################################################


        # Log some task information once
        self.buildLog(["STATE", "TARGET", "X", str(0.5)])
        self.buildLog(["STATE", "TARGET", "Y", str(0.5)])
        self.buildLog(["STATE", "TARGET", "RADIUS",
                       str(self.parameters['targetradius'])])
        msg = _('AUTO') if self.parameters['automaticsolver'] else _('MANUAL')
        self.buildLog(["STATE", "", "MODE", msg])

    def onUpdate(self):

        if self.parameters['displayautomationstate']:
            self.refreshModeLabel()
        else:
            self.modeLabel.hide()

        if self.parameters['resetperformance'] is not None:
            if self.parameters['resetperformance'] in ['last', 'global']:
                for i in self.performance[self.parameters['resetperformance']]:
                    self.performance[self.parameters['resetperformance']][i] = 0
            else:
                self.parent().showCriticalMessage(_("%s : wrong argument in track;resetperformance") % self.parameters['resetperformance'])

            self.parameters['resetperformance'] = None

        # Preallocate x and y input variables
        x_input, y_input = 0, 0

        # Compute next cursor coordinates (x,y)
        current_X, current_Y = self.widget.moveCursor()
        # print(f'current_X:{current_X}, current_Y:{current_Y}')
        # If automatic solver : always correct cursor position
        if self.parameters['automaticsolver']:
            x_input, y_input = self.widget.getAutoCompensation()

        # Else record manual compensatory movements
        else:
            # Retrieve potentials joystick inputs (x,y)
            # x_input, y_input = self.joystick_input()
            ############### FOR KEYBOARD INPUT #########################
            x_input, y_input = self.parameters['coordinates']
            self.parameters['coordinates'] = (0,0)
            # print(f'X_input:{x_input}, Y_input:{y_input}')
            ############################################################

            # If assisted solver : correct cursor position only if joystick
            # inputs something
            if self.parameters['assistedsolver']:
                if any([this_input != 0 for this_input in [x_input, y_input]]):
                    x_input, y_input = self.widget.getAutoCompensation()

        # Modulate cursor position with potentials joystick inputs
        current_X += x_input
        current_Y += y_input
        # print(f'new_X:{current_X}, new_Y:{current_Y}')
        # print('\n')
        # Refresh the display
        self.widget.refreshCursorPosition(current_X, current_Y)

        # Constantly log the cursor coordinates
        self.buildLog(["STATE", "CURSOR", "X", str(current_X)])
        self.buildLog(["STATE", "CURSOR", "Y", str(current_Y)])

        # Record performance
        for perf_cat, perf_val in self.performance.items():
            if self.widget.isCursorInTarget():
                perf_val['time_in_ms'] += self.parameters['taskupdatetime']
            else:
                # write the current time in ms to the file
                dt_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                file.write("OUT: "+dt_string+"\n")
                perf_val['time_out_ms'] += self.parameters['taskupdatetime']

            current_deviation = self.widget.returnAbsoluteDeviation()
            perf_val['points_number'] += 1
            perf_val['deviation_mean'] = perf_val['deviation_mean'] * ((perf_val['points_number']-1) / float(perf_val['points_number'])) + current_deviation * (float(1) / perf_val['points_number'])

        global dash_flag
        if not self.parameters['automaticsolver']:
            file.write(str(self.performance)+'\n')
        else:
            dash_flag = 1

        if dash_flag==1:
            dash_flag = 0
            file.write('AUTO\n')


    def keyEvent(self,key_pressed,event=None):
        numpad_mod = int(event.modifiers()) & QtCore.Qt.KeypadModifier
        if key_pressed == QtCore.Qt.Key_5 and numpad_mod:
            #DOWN movement
            self.parameters['coordinates'] = (0,0.1)
        if key_pressed == QtCore.Qt.Key_8 and numpad_mod:
            #UP movement
            self.parameters['coordinates'] = (0,-0.1)
        if key_pressed == QtCore.Qt.Key_6 and numpad_mod:
            #RIGHT movement
            self.parameters['coordinates'] = (0.1,0)
        if key_pressed == QtCore.Qt.Key_4 and numpad_mod:
            #LEFT movement
            self.parameters['coordinates'] = (-0.1,0)


    def joystick_input(self):
        if self.my_joystick:
            pygame.event.pump()
            # Apply a joystickforce factor to joystick input to obtain a
            # smoother movement
            current_force = self.parameters['taskupdatetime'] * (float(self.parameters['joystickforce'])/1000)
            return self.my_joystick.get_axis(0) * current_force, self.my_joystick.get_axis(1) * current_force
        else:
            return (0, 0)

    def refreshModeLabel(self):
        if self.parameters['automaticsolver']:
            # self.modeLabel.setText("<b>%s</b>" % _('AUTO ON'))
            self.modeLabel.setText("AUTO ON")
            self.modeLabel.setStyleSheet("color:blue;font-size: 18pt;")

        elif self.parameters['assistedsolver']:
            self.modeLabel.setText("<b>%s</b>" % _('ASSIST ON'))
        else:
            self.modeLabel.setText("MANUAL")
            self.modeLabel.setStyleSheet("color:red;font-size: 18pt;")
        self.modeLabel.show()

    def buildLog(self, thisList):
        thisList = ["TRACK"] + thisList
        self.parent().mainLog.addLine(thisList)
