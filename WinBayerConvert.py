#!/usr/bin/env python3

## fits_debayer_swap - BayerConvert
## Copyright (C) 2021 Paul de Backer
##
## 
## BayerConvert is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## BayerConvert is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with fits_calibration.  If not, see <http://www.gnu.org/licenses/>.



from astropy.io import fits
import glob, sys, os
import fnmatch
import PySimpleGUI as sg


def HandleFitsFile (fName, fromPat, toPat):
    
    try:
        image, header = fits.getdata(fName, header=True)
    
        if header['BAYERPAT'] == fromPat:
            print(fName + '...', end='')
            image=image[::-1,::-1]
            header['BAYERPAT'] = toPat
            fits.writeto(fName, image, header, overwrite=True)
            print ('Done')
            return True

    except:
        return False

    return False

helptxt = 'Walks through a folder and searches for files with fits extension. For files with selected BayerPattern, the image is rotated and BayerPattern in the header updated'

selfolder = os.getcwd()
menu_def = [['Actions', ['Exit']],           
            ['Help', ['What?', 'About...']], ]


VERSION = 'A.00.01.004'
A_BOUT = 'Debayer Swap. Version: ' + VERSION + '\n(c) Paul De Backer - 2021'



layout = [  [sg.Menu(menu_def, tearoff=True)],
            [sg.Text('Conversion Folder:', size=(15,1)), sg.Text(selfolder, size=(36,1)), sg.FolderBrowse(enable_events=True, key='_OUTPUT_' )],
            [sg.Checkbox('Recursive', key='_RECURSIVE_')],
            [sg.Radio('RGGB->BGGR', 'R1', key='_RGGB', default=True), sg.Radio('BGGR->RGGB', 'R1', key='_BGGR'), sg.Radio('GBRG->GRBG','R1', key='_GBRG'), sg.Radio('GRBG->GBRG', 'R1', key='_GRBG')],
            [sg.Output(size=(76, 25), font=('Courier', 8), key='-RESULT-')],
            [sg.Button(' Start ', key='-START-'), sg.Button('Cancel', key='-CANCEL-', visible=False)] ]

ProcessedFiles = 0

window = sg.Window('Bayer Swap', layout, default_element_size=(40, 1), grab_anywhere=False)
while True:
    event, values = window.Read()

    if event in (None, 'Exit'):    
        break
    fP = 'None'
    tP = 'None'
    if event == '-START-':
        ProcessedFiles = 0
        if values['_BGGR']:
            fP = 'BGGR'
            tP = 'RGGB'
        elif values['_RGGB']:
            fP = 'RGGB'
            tP = 'BGGR'
        elif values['_GBRG']:
            fP = 'GBRG'
            tP = 'GRBG'
        elif values['_GRBG']:
            fP = 'GRBG'
            tP = 'GBGG'

        print ('starting ' + fP + ' to '+ tP)
    
        window.element('-START-').Update(disabled=True)
        
        selfolder = values['_OUTPUT_']
        
        if selfolder == '' : selfolder = os.getcwd()
        
        try:
            if values['_RECURSIVE_']:
                for root, mydir, files in os.walk(selfolder, topdown=True):
                    
                    for items in fnmatch.filter(files, '*.fits'):
                        if HandleFitsFile (os.path.join(root, items), fP, tP):
                            ProcessedFiles = ProcessedFiles + 1
            else:
                for f in (glob.glob(selfolder + '/*.fits')):
                    if HandleFitsFile (os.path.join('', f), fP, tP) == True:
                        ProcessedFiles = ProcessedFiles + 1
       
        except:
            print("Unexpected error:", sys.exc_info()[0])

        print ( 'Processed:', ProcessedFiles, 'files' )
        window.element('-START-').Update(disabled=False)
    
    if event == 'About...':
        sg.PopupOK(A_BOUT, title='Fits Calibration ' + VERSION)

    if event == 'What?':
        sg.PopupOK(helptxt)

window.Close()
