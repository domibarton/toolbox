# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib import messages
import re


class IndexView(TemplateView):
    '''
    RC Hobby index view.
    '''

    # Name / path of the rendered HTML template.
    template_name = 'rchobby/index.html'


class HyperionView(TemplateView):
    '''
    View to generate Hyperion memoryset.
    '''

    # Only allow POST requests.
    http_method_names = ('post',)

    # Name / path of the rendered HTML template.
    template_name = 'rchobby/hyperion.html'

    # All attributes of a memoryset entry with its corresponding RegEx pattern.
    memoryset_attributes = (
        ('batteryType', re.compile(r'batteryType="(\w+)"')),
        ('batteryCells', re.compile(r'batteryCells="(\d+)"')),
        ('batteryCapacity', re.compile(r'batteryCapacity="(\d+)"')),
        ('ChargeCurrent', re.compile(r'ChargeCurrent="(\d+)"')),
        ('DischargeCurrent', re.compile(r'DischargeCurrent="(\d+)"')),
        ('DischargeCutoffVoltage', re.compile(r'DischargeCutoffVoltage="(\w+)"')),
        ('ChargeDeltaPeak', re.compile(r'ChargeDeltaPeak="(\d+)"')),
        ('CutOffTemperature', re.compile(r'CutOffTemperature="(\d+)"')),
        ('TCS_Capacity', re.compile(r'TCS_Capacity="(\d+)"')),
        ('ChargeSafetyTimer', re.compile(r'ChargeSafetyTimer="(\d+)"')),
        ('PrePeakDelay', re.compile(r'PrePeakDelay="(\d+)"')),
        ('TrickleCurrent', re.compile(r'TrickleCurrent="(\d+)"')),
        ('TCS_EndAction', re.compile(r'TCS_EndAction="(\d+)"')),
        ('TVS_AdjustVoltage', re.compile(r'TVS_AdjustVoltage="(\d+)"')),
        ('MemoryName', re.compile(r'MemoryName="([^"]*)"')),
        ('PB_FloatingVolt', re.compile(r'PB_FloatingVolt="(\d+)"')),
        ('PB_BatteryChargeVolt', re.compile(r'PB_BatteryChargeVolt="(\d+)"')),
        ('TCS_StoragePercent', re.compile(r'TCS_StoragePercent="(\d+)"')),
    )

    # All available battery types.
    # IMPORTANT: Please consider the order, the checksum depends on it!
    battery_types = (
        'NiCd',
        'NiMh',
        'LiIo',
        'LiPo',
        'LiFe',
        'Pb'
    )

    def _parse_memoryset_file(self, file):
        '''
        Parses the uploaded memoryset file and returns the charger ID and
        memoryset for the template context.
        '''
        # Read file and split lines.
        lines      = file.read().split('\n')
        first_line = lines.pop(0)
        last_line  = lines.pop()

        # Extract chargerID from first line.
        m         = re.search(r'chargerID="([0-9a-f]+)"', first_line)
        chargerID = m.group(1)

        # Extract all memoryset entries.
        memoryset = []
        for line in lines:
            memory = {}
            for a, r in self.memoryset_attributes:
                m         = r.search(line)
                memory[a] = m.group(1)
            memoryset.append(memory)

        # Return chargerID and memoryset entries.
        return chargerID, memoryset

    def _get_post_data(self):
        '''
        Returns the charger ID and memoryset from the received POST variables.
        '''
        # Cache it, will be called in post() and get_context_data() simultaneously.
        if not hasattr(self, '_post_data'):

            # Get charger ID.
            chargerID = self.request.POST.get('chargerID')

            # Get rest of the data values as lists.
            data = {}
            for a, r in self.memoryset_attributes:
                data[a] = self.request.POST.getlist(a + '[]')

            # Convert to proper memoryset.
            l         = len(data['batteryCapacity'])
            memoryset = []
            for i in range(l):
                memory = {}
                for attr, values in data.iteritems():
                    memory[attr] = values[i]
                memoryset.append(memory)

            self._post_data = chargerID, memoryset

        return self._post_data

    def _generate_memoryset(self, chargerID, memoryset):
        '''
        Generates the memoryset from the POST variables.
        '''
        # Fetch data from POST request / variables.
        data = {'chargerID': self.request.POST.get('chargerID')}
        for a, r in self.memoryset_attributes:
            data[a] = self.request.POST.getlist(a + '[]')

        # Get memoryset size / length.
        l = len(data['batteryCapacity'])

        # Initialize <MEMORYSET…>.
        now       = timezone.now()
        memoryset = '<MEMORYSET chargerID="{}" channel="0" memoryCount="{}" creatorVersion="{}" date="{}">\r\n'.format(
            data['chargerID'],
            l,
            now.strftime('%Y-%m-%d'),
            now.strftime('%d/%m/%Y %H:%M:%S')
        )

        # Create <MEMORY…> entries.
        for i in range(l):

            # Calculate checksum.
            checksum  = self.battery_types.index(data['batteryType'][i])
            checksum *= int(data['batteryCells'][i])
            checksum += int(data['batteryCapacity'][i])
            checksum += int(data['ChargeCurrent'][i])
            checksum += int(data['DischargeCurrent'][i])
            checksum += 370 + (int(data['DischargeCutoffVoltage'][i]) - 3700)
            checksum -= int(data['ChargeDeltaPeak'][i])
            checksum += 50 - int(data['CutOffTemperature'][i])
            checksum += 100 - int(data['TCS_Capacity'][i])
            checksum += 100 - int(data['ChargeSafetyTimer'][i])
            checksum -= int(data['PrePeakDelay'][i])
            checksum -= int(data['TrickleCurrent'][i])
            checksum -= int(data['TCS_EndAction'][i])
            checksum += 1000 - (int(data['TVS_AdjustVoltage'][i]) - 1000)
            checksum -= 13200 - int(data['PB_FloatingVolt'][i])
            checksum += 14280 - int(data['PB_BatteryChargeVolt'][i])

            # Build <MEMORY…> entry.
            memory = '  <MEMORY '
            for a, r in self.memoryset_attributes:
                memory += '{}="{}" '.format(a, data[a][i])
            memory += 'CheckSum="{}" />'.format(checksum)

            # Add <MEMORY…> entry to <MEMORYSET…>.
            memoryset += '{}\r\n'.format(memory)

        # Finalize <MEMORYSET…>.
        memoryset += '</MEMORYSET>'

        return memoryset

    def post(self, request):
        '''
        Handles all POST requests. In our case this means handling the uploaded
        file and
        '''
        # Get context data.
        try:
            context = self.get_context_data()
        except Exception as e:
            messages.error(request, e)
            return redirect(request.META.get('HTTP_REFERER'))

        # Generate memoryset file in case we got the "generate" POST variable.
        if request.POST.get('generate'):
            try:
                # Generate new memoryset (text/plain content).
                memoryset = self._generate_memoryset(
                    chargerID=context['chargerID'],
                    memoryset=context['memoryset']
                )

                # Create response object.
                response = HttpResponse(
                    content=memoryset,
                    content_type='text/plain'
                )
                response['Content-Disposition'] = 'attachment; filename=memoryset.eos'

                # Return response.
                return response

            # Error while generating the new file so there's an invalid value.
            except ValueError as e:
                messages.error(request, 'ERROR: Invalid value found! Exception was "{}".'.format(e))

        # Render HTML view.
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        '''
        Returns the context data for the template. In our case this means in
        case of a POST request the uploaded memoryset file will be parsed or
        the received POST values will be prepared.
        '''
        context = super(HyperionView, self).get_context_data(**kwargs)
        request = self.request

        # Nothing to do in case we've no POST request.
        if request.method != 'POST':
            return context

        # In case we found a file in the POST request, parse it!
        file = request.FILES.get('file')
        if file:
            try:
                chargerID, memoryset = self._parse_memoryset_file(file)
            except AttributeError:
                raise Exception('ERROR: Could not parse the uploaded file! Is it really a Hyperion Control & Data Suite memoryset file?')

        # In case we found the "generate" POST variable, get POST data.
        elif request.POST.get('generate'):
            chargerID, memoryset = self._get_post_data()

        # If we reached this point, no file and no "generate" variable was found.
        # Therefore something must be wrong.
        else:
            raise Exception('ERROR: No uploaded file and no POST data was found!')

        context.update({
            'chargerID': chargerID,
            'memoryset': memoryset,
            'battery_types': self.battery_types
        })

        return context
