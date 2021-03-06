
from PyQt5 import QtWidgets, QtCore, QtGui


class TreeView(QtWidgets.QTreeView):
    def __init__(self, parent, accepted_type, unique_elements=True):
        QtWidgets.QTreeView.__init__(self, parent)
        self.accepted_type = accepted_type
        self.unique_elements = unique_elements
        self.setDragEnabled(True)
        self.setAcceptDrops(True)

    def startDrag(self, dropAction):
        mime = QtCore.QMimeData()
        mime.setData('accepted_type', self.accepted_type.encode('utf-8'))
        index = self.currentIndex()
        item = index.model().itemFromIndex(index)
        mime.setText(item.text())
        #mime.setData('application/x-item', '???')

        #print('Start dragging')
        drag = QtGui.QDrag(self)
        drag.setMimeData(mime)
        drag.exec(QtCore.Qt.CopyAction)#start(QtCore.Qt.CopyAction)#(QtCore.Qt.CopyAction)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("accepted_type"):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if (event.mimeData().data('accepted_type').data().decode("utf-8") == self.accepted_type):
            event.accept()
        else:
            event.ignore()    

    def dropEvent(self, event):
        #if self.accepted_type = event.mimeData().data('accepted_type'):
        #QtWidgets.QTreeView.dropEvent(self, event)
        #if event.isAccepted():
        #    print('dropEvent', hasattr(self, 'x'))
        #print('Formats: {}'.format(event.mimeData().formats()))
        #print('Mime: {}'.format(event.mimeData().data('application/x-qstandarditemmodeldatalist')))
        #data = event.mimeData().data('application/x-qabstractitemmodeldatalist')

        exists = False
        curr_item_text = event.mimeData().text()
        if self.unique_elements:
            for i in range(self.model().rowCount()):
                if self.model().item(i).text() == curr_item_text:
                    exists = True
                    break

        if not exists:
            event.acceptProposedAction()
            item = QtGui.QStandardItem()
            item.setText(curr_item_text)
            parent = self.model().invisibleRootItem()
            parent.appendRow(item)
            QtWidgets.QTreeView.dropEvent(self, event)



