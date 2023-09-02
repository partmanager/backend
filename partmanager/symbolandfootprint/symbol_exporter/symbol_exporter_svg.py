from .symbol_exporter_base import SymbolExporterBase
import drawSvg as svg


class SymbolExporterSVG(SymbolExporterBase):
    def __init__(self, name, symbol_data):
        self.name = name
        self.symbol_data = symbol_data
        self.drawing = svg.Drawing(50, 50, origin='center')
        self.process()

    def add_pin(self, pin):
        if pin['rotation'] == 0:
            x2 = pin['x1'] + pin['length']
            y2 = pin['y1']
        elif pin['rotation'] == 180:
            x2 = pin['x1'] - pin['length']
            y2 = pin['y1']
        self.drawing.append(svg.Line(pin['x1'], pin['y1'], x2, y2, stroke='black', stroke_width=1, fill='none'))

    def add_rectangle(self, parameters):
        width = parameters['x2'] - parameters['x1']
        height = parameters['y2'] - parameters['y1']
        fill_opacity = 0 if parameters['fill'] is None else 1
        self.drawing.append(svg.Rectangle(parameters['x1'], parameters['y1'], width, height,
                                     stroke='black', stroke_width=1, fill_opacity=fill_opacity))

    def process(self):
        for pin in self.symbol_data['pins']:
            print("Adding pin:", pin)
            self.add_pin(pin)
        for body_part in self.symbol_data['body']:
            if body_part['object'] == 'rectangle':
                self.add_rectangle(body_part['parameters'])

    def export_to_file(self, path):
        self.drawing.saveSvg(path)
