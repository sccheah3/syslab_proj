import django_tables2 as tables
from system_test_app.models import System

class SystemTable(tables.Table):
    #class Meta:
        #model = System
        #template_name = 'django_tables2/bootstrap.html'

    motherboard_model = tables.Column()
    bios_date = tables.Column()
    ipmi_version = tables.Column()
    processor_info = tables.Column()
    dimm = tables.Column(accessor="dimm_data", orderable=False)
    linpack_theoretical_score = tables.Column()
    linpack_score = tables.Column(accessor="linpack_actual_data", orderable=False)
    date_added = tables.Column()