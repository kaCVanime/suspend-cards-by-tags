from aqt import mw, operations
from aqt.utils import ask_user, showInfo
from aqt.qt import *
from .flow_layout import FlowLayout
from .tag import ClosableTag
from .checkable_combobox import CheckableComboBox
class MainWindow(QWidget):
    selected_deck = ""
    bad_tags = set()
    good_tags = set()
    bad_tag_widgets = []
    good_tag_widgets = []
    tags = []
    decks = []
    bad_all_checked = False
    good_all_checked = False

    def __init__(self, decks, tags):
        super(MainWindow, self).__init__()

        self.setFixedWidth(500)

        self.decks = decks
        self.tags = tags

        self.v_layout = QVBoxLayout(self)

        self.groupbox_deck = QGroupBox("1. Choose Deck")
        self.groupbox_deck.setFixedHeight(80)
        self.form_layout_deck = QFormLayout(self)
        self.combobox_deck = QComboBox(self)

        self.groupbox_bad = QGroupBox("2. Suspend cards that has tag:")
        self.form_layout_bad = QFormLayout(self)
        self.checkbox_bad_all = QCheckBox(self)
        self.combobox_bad = CheckableComboBox(self)
        self.scroll_area_bad = QScrollArea(self)
        self.scroll_area_bad_widget = QWidget(self.scroll_area_bad)
        self.h_layout_bad_selected = FlowLayout(self.scroll_area_bad_widget)
        self.label_bad_total = QLabel("0")

        self.groupbox_good = QGroupBox("3. Then Unsuspend cards that has tag:")
        self.form_layout_good = QFormLayout(self)
        self.checkbox_good_all = QCheckBox(self)
        self.combobox_good = CheckableComboBox(self)
        self.scroll_area_good = QScrollArea(self)
        self.scroll_area_good_widget = QWidget(self.scroll_area_good)
        self.h_layout_good_selected = FlowLayout(self.scroll_area_good_widget)
        self.label_good_total = QLabel("0")

        self.start_btn = QPushButton(self)
        self.start_btn.setText("Start")
        self.start_btn.setFixedHeight(50)

        self.init_layout()
        self.init_combobox()

    def init_layout(self):
        self.v_layout.addWidget(self.groupbox_deck)
        self.v_layout.addWidget(self.groupbox_bad)
        self.v_layout.addWidget(self.groupbox_good)
        self.v_layout.addWidget(self.start_btn)

        self.groupbox_deck.setLayout(self.form_layout_deck)
        self.form_layout_deck.addRow("deck", self.combobox_deck)

        self.groupbox_bad.setLayout(self.form_layout_bad)
        self.form_layout_bad.addRow("Suspend all tagged cards", self.checkbox_bad_all)
        self.form_layout_bad.addRow("select tag", self.combobox_bad)
        self.form_layout_bad.addRow("selected", self.scroll_area_bad)
        self.form_layout_bad.addRow("Total", self.label_bad_total)
        self.scroll_area_bad_widget.setMinimumWidth(50)
        self.scroll_area_bad_widget.setContentsMargins(5, 5, 5, 5)
        self.scroll_area_bad.setWidget(self.scroll_area_bad_widget)
        self.scroll_area_bad.setWidgetResizable(True)

        self.groupbox_good.setLayout(self.form_layout_good)
        self.form_layout_good.addRow("Unsuspend all tagged cards", self.checkbox_good_all)
        self.form_layout_good.addRow("select tag", self.combobox_good)
        self.form_layout_good.addRow("selected", self.scroll_area_good)
        self.form_layout_good.addRow("Total", self.label_good_total)
        self.scroll_area_good_widget.setMinimumWidth(50)
        self.scroll_area_good_widget.setContentsMargins(5, 5, 5, 5)
        self.scroll_area_good.setWidget(self.scroll_area_good_widget)
        self.scroll_area_good.setWidgetResizable(True)

        self.setLayout(self.v_layout)

        self.checkbox_bad_all.stateChanged.connect(self.on_bad_all_checked)
        self.checkbox_good_all.stateChanged.connect(self.on_good_all_checked)

        self.start_btn.clicked.connect(self.confirm)

    def init_combobox(self):
        self.combobox_deck.addItems(self.decks)
        self.combobox_deck.currentIndexChanged.connect(self.on_deck_selected)
        self.on_deck_selected()

        self.combobox_bad.addItems(self.tags)
        self.combobox_bad.changed.connect(self.on_bad_tag_selected)

        self.combobox_good.addItems(self.tags)
        self.combobox_good.changed.connect(self.on_good_tag_selected)

    def on_deck_selected(self):
        label = self.combobox_deck.currentText()
        self.selected_deck = label
        self.update_count(self.good_all_checked, self.good_tags, self.label_good_total)
        self.update_count(self.bad_all_checked, self.bad_tags, self.label_bad_total)

    def on_bad_all_checked(self):
        self.bad_all_checked = self.checkbox_bad_all.isChecked()
        self.update_count(self.bad_all_checked, self.bad_tags, self.label_bad_total)

    def on_good_all_checked(self):
        self.good_all_checked = self.checkbox_good_all.isChecked()
        self.update_count(self.good_all_checked, self.good_tags, self.label_good_total)

    def on_tag_selected(self, widget_list, tag_set, layout, is_all_checked, count_layout, label):
        if label not in tag_set:
            tag = ClosableTag(label)
            tag.closed.connect(lambda: self.on_tag_closed(is_all_checked, tag_set, label, count_layout))
            widget_list.append(tag)
            layout.addWidget(tag)
            tag_set.add(label)
            self.update_count(is_all_checked, tag_set, count_layout)
        else:
            for widget in widget_list:
                if widget.tag == label:
                    widget.close_tag()
                    widget_list.remove(widget)
                    break


    def on_tag_closed(self, is_all_checked, tag_set, label, count_layout):
        tag_set.remove(label)
        self.update_count(is_all_checked, tag_set, count_layout)
        pass

    def on_good_tag_selected(self, text):
        self.on_tag_selected(
            widget_list=self.good_tag_widgets,
            tag_set=self.good_tags,
            layout=self.h_layout_good_selected,
            is_all_checked=self.good_all_checked,
            count_layout=self.label_good_total,
            label=text
        )


    def on_bad_tag_selected(self, text):
        self.on_tag_selected(
            widget_list=self.bad_tag_widgets,
            tag_set=self.bad_tags,
            layout=self.h_layout_bad_selected,
            is_all_checked=self.bad_all_checked,
            count_layout=self.label_bad_total,
            label=text
        )

    def update_count(self, is_all_checked, tags, label_widget):
        if not is_all_checked and not len(tags):
            label_widget.setText("0")
            return

        query = self.get_query(is_all_checked, tags)

        cids = mw.col.find_cards(query)

        label_widget.setText(str(len(cids)))

    def get_query(self, is_all_checked, tags):
        if not is_all_checked and not len(tags):
            return False
        query = f"deck:{self.selected_deck} "
        if is_all_checked:
            query += "-tag:none"
        else:
            query += self.get_or_query(tags)
        return query

    # def escape_special_chars(self, input_string):
    #     special_chars = r'[\^\$\.\|\?\*\+\(\)\{\}\[\]\\\_]'
    #     return re.sub(special_chars, lambda match: f'\\{match.group(0)}', input_string)

    def get_or_query(self, tags):
        if not len(tags):
            return ""
        # return "({})".format(" OR ".join([f"tag:{self.escape_special_chars(tag)}" for tag in tags]))
        return "({})".format(" OR ".join([f"tag:{tag}" for tag in tags]))

    def confirm(self):
        ask_user("confirm batch suspend?", self.start)

    def start(self, confirm):
        if confirm:
            suspend_query = self.get_query(self.bad_all_checked, self.bad_tags)
            suspend_cids = mw.col.find_cards(suspend_query) if suspend_query else []
            unsuspend_query = self.get_query(self.good_all_checked, self.good_tags)
            unsuspend_cids = mw.col.find_cards(unsuspend_query) if unsuspend_query else []
            to_suspend_cids = [cid for cid in suspend_cids if cid not in unsuspend_cids]

            self.suspend(to_suspend_cids)
            self.unsuspend(unsuspend_cids)

            showInfo("Done")

    def suspend(self, cids, suspend=True):
        for id in cids:
            if self.is_suspended(id) == suspend:
                cids.remove(id)

        if len(cids) == 0:
            return False

        scheduler = mw.col.sched
        mw.requireReset()
        if suspend:
            scheduler.suspendCards(cids)
        else:
            scheduler.unsuspendCards(cids)

        return True

    def unsuspend(self, cids):
        self.suspend(cids, False)

    def is_suspended(self, id):
        card = mw.col.get_card(id)
        return card.queue == -1


def show_window():
    decks = mw.col.decks.allNames()
    tags = mw.col.tags.all()
    mw.suspendByTagsMainWindow = MainWindow(decks, tags)
    mw.suspendByTagsMainWindow.show()


# create a new menu item, "test"
action = QAction("Batch suspend card by tags", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(show_window)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
