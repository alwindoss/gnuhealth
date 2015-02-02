import server.fhir as supermod
from StringIO import StringIO
from operator import attrgetter

try:
    from flask import url_for
    RUN_FLASK=True
except:
    from .datastore import dumb_url_generate
    RUN_FLASK=False

class DiagnosticReport_Map:
    """
    The model mapping for the DiagnosticReport Resource
    """
    # Must be completed (i.e., have date)
    root_search=[('date_analysis', '!=', None)]

    # No other models, just use row id
    url_prefixes={}

    model_mapping={
            'gnuhealth.lab': {
                'subject': 'patient',
                'performer': 'pathologist',
                'conclusion': 'results', #or diagnosis?
                'codedDiagnosis': 'diagnosis',
                'result': 'critearea',
                'date': 'date_analysis',
                'code': 'test.code',
                'name': 'test.name'}
                }
    resource_search_params={
                    '_id': 'token',
                    '_language': None,
                    'date': None,
                    'diagnosis': None, 
                    'identifier': None,
                    'image': None,
                    'issued': 'date',
                    'name': 'token',
                    'performer': 'reference',
                    'request': None,
                    'result': 'reference',
                    'service': None,
                    'specimen': None,
                    'status': None,
                    'subject': 'reference'}

    # Reference parameters to resource type
    chain_map={
            'subject': 'Patient',
            'result': 'Observation',
            'performer': 'Practitioner'}

    search_mapping={
                    '_id': ['id'],
                    'issued': ['date_analysis'],
                    'name': ['test.code'],
                    'name:text': ['test.name'],
                    'performer': ['pathologist'],
                    'result': ['critearea'],
                    'subject': ['patient']}

class health_DiagnosticReport(supermod.DiagnosticReport, DiagnosticReport_Map):
    """
    Class that manages the interface between FHIR Resource DiagnosticReport
        and GNU Health
    """
    def __init__(self, *args, **kwargs):
        rec = kwargs.pop('gnu_record', None)
        super(health_DiagnosticReport, self).__init__(*args, **kwargs)
        if rec:
            self.set_gnu_diagnostic_report(rec)

    def set_gnu_diagnostic_report(self, diagnostic_report):
        self.diagnostic_report = diagnostic_report
        self.model_type = self.diagnostic_report.__name__

        # Only certain models
        if self.model_type not in self.model_mapping:
            raise ValueError('Not a valid model')

        self.map = self.model_mapping[self.model_type]

        self.__import_from_gnu_diagnostic_report()

    def __import_from_gnu_diagnostic_report(self):
        if self.diagnostic_report:
            self.__set_gnu_identifier()
            self.__set_gnu_result()
            self.__set_gnu_performer()
            self.__set_gnu_subject()
            self.__set_gnu_name()
            self.__set_gnu_issued()
            self.__set_gnu_conclusion()
            self.__set_feed_info()

    def __set_gnu_identifier(self):
        if self.diagnostic_report:
            obj, patient, time = attrgetter(self.map['name'], self.map['subject'], self.map['date'])(self.diagnostic_report)

            if obj and patient and time:
                label = '{0} for {1} on {2}'.format(obj, patient.name.rec_name, time.strftime('%Y/%m/%d'))
                if RUN_FLASK:
                    value = url_for('dr_record', log_id=self.diagnostic_report.id)
                else:
                    value = dumb_url_generate(['DiagnosticReport',
                                                self.diagnostic_report.id])
                ident = supermod.Identifier(
                            label=supermod.string(value=label),
                            value=supermod.string(value=value))
                self.set_identifier(ident)

    def __set_feed_info(self):
        ''' Sets the feed-relevant info
        '''
        if self.diagnostic_report:
            self.feed={'id': self.diagnostic_report.id,
                    'published': self.diagnostic_report.create_date,
                    'updated': self.diagnostic_report.write_date or self.diagnostic_report.create_date,
                    'title': self.diagnostic_report.rec_name
                        }

    def __set_gnu_name(self):
        if self.diagnostic_report:
            try:
                conc = supermod.CodeableConcept()
                conc.coding=[supermod.Coding()]
                conc.coding[0].display=supermod.string(value=attrgetter(self.map['name'])(self.diagnostic_report))
                conc.coding[0].code = supermod.code(value=attrgetter(self.map['code'])(self.diagnostic_report))
                self.set_name(conc)
            except:
                # If you don't know what is being tested,
                #   the data is useless
                raise ValueError('No test coding info')

    def __set_gnu_issued(self):
        if self.diagnostic_report:
            try:
                time=attrgetter(self.map['date'])(self.diagnostic_report)
                instant = supermod.instant(value=time.strftime("%Y-%m-%dT%H:%M:%S"))
                self.set_issued(instant)
            except:
                # If there is no date attached, this report is either not done
                #  or useless
                raise ValueError('No date')

    def __set_gnu_result(self):
        if self.diagnostic_report:
            try:
                for test in attrgetter(self.map['result'])(self.diagnostic_report):
                    if RUN_FLASK:
                        uri = url_for('obs_record', log_id=test.id)
                    else:
                        uri = dumb_url_generate(['Observation', test.id])
                    display = test.rec_name
                    ref=supermod.ResourceReference()
                    ref.display = supermod.string(value=display)
                    ref.reference = supermod.string(value=uri)
                    self.add_result(ref)
            except:
                # No data = useless
                raise ValueError('No data')
            finally:
                # No data = useless
                if len(self.get_result()) == 0:
                    raise ValueError('No data')

    def __set_gnu_performer(self):
        if self.diagnostic_report:
            try:
                p = attrgetter(self.map['performer'])(self.diagnostic_report)
                if RUN_FLASK:
                    uri = url_for('hp_record', log_id=p.id)
                else:
                    uri = dumb_url_generate(['Practitioner', p.id])
                display = p.name.rec_name
                ref=supermod.ResourceReference()
                ref.display = supermod.string(value=display)
                ref.reference = supermod.string(value=uri)
            except:
                # Not absolutely needed, so continue execution
                pass
            else:
                self.set_performer(ref)

    def __set_gnu_subject(self):
        if self.diagnostic_report:
            try:
                patient = attrgetter(self.map['subject'])(self.diagnostic_report)
                if RUN_FLASK:
                    uri = url_for('pat_record', log_id=patient.id)
                else:
                    uri = dumb_url_generate(['Patient', patient.id])
                display = patient.rec_name
                ref=supermod.ResourceReference()
                ref.display = supermod.string(value=display)
                ref.reference = supermod.string(value=uri)
                self.set_subject(ref)
            except:
                # Without subject, useless information
                raise ValueError('No subject')

    def __set_gnu_conclusion(self):
        if self.diagnostic_report:
            try:
                text = attrgetter(self.map['conclusion'])(self.diagnostic_report)
                if text:
                    conclusion = supermod.string(value=text)
                    self.set_conclusion(conclusion)
            except:
                # Not absolutely necessary
                pass

    def export_to_xml_string(self):
        """Export"""
        output = StringIO()
        self.export(outfile=output, namespacedef_='xmlns="http://hl7.org/fhir"', pretty_print=False, level=4)
        content = output.getvalue()
        output.close()
        return content
supermod.DiagnosticReport.subclass=health_DiagnosticReport

class health_DiagnosticReport_Image(supermod.DiagnosticReport_Image):
    pass

class health_DiagnosticReportStatus(supermod.DiagnosticReportStatus):
    pass
