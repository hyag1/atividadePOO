# from reportlab.pdfgen import canvas
# import datetime
# import random
#
# def generatePdf(nome,aluno_id,disciplinas):
#     logo = "python_logo.png"
#     data_atual = datetime.today().strftime('%d/%m/%Y')
#     im = Image(logo, 2 * inch, 2 * inch)
#     x = random.randrange(1,99999)
#     nome_pdf = 'declaracao_'+x+'_gerada'
#     pdf = canvas.Canvas('{}{}.pdf'.format(nome_pdf, nome))
#     pdf.drawString(30, 750, 'D E C L A R A Ç Ã O')
#     pdf.drawString(30, 735, 'UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE')
#     pdf.drawString(480, 750, 'DATA: ' + str(data_atual))
#     pdf.line(480, 747, 580, 747)
#     pdf.drawString(400, 725, 'ALUNO:')
#     pdf.drawString(500, 725, nome)
#     pdf.line(480, 723, 580, 723)
#
#     pdf.drawString(30, 703, 'MATRICULA:')
#     pdf.line(120, 700, 580, 700)
#     pdf.drawString(120, 703, aluno_id)
#
#     pdf.drawString(30, 680, 'MATRICULADO NAS DISCILPINAS:')
#     pdf.line(300, 680, 580, 678)
#     pdf.drawString(300, 683, disciplinas)
#     pdf.showPage()
#     pdf.save()
#     print('{}.pdf criado com sucesso!'.format(nome_pdf))

import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import random

x = random.randrange(0, 99999)
name_path = "declaracao/comprovante_" + str(x) + ".pdf"
doc = SimpleDocTemplate(name_path, pagesize=letter,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)


def criar_pdf(name,id):
    Story = []
    logo = "public/logo.png"
    full_name = str(name)
    formatted_time = time.ctime()
    im = Image(logo, 5.5 * inch, 1.5 * inch)
    matricula = str(id)
    Story.append(im)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '%s' % formatted_time
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    # Create return address
    ptext = '%s' % full_name
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = 'Querido %s:' % full_name.split()[0].strip()
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = 'Declaramos, para os fins a que se fizerem necessários, que %s é aluno(a) vinculado(a) a este(a) universidade, sob o número ' \
            '20210_%s, no curso de ENGENHARIA DE TELECOMUNICAÇÕES - NATAL.' % (
        full_name,
        matricula)
    Story.append(Paragraph(ptext, styles["Justify"]))
    doc.build(Story)
    return name_path
