from __future__ import with_statement

import os
import json
import re
from functools import partial
from pprint import pprint

from flask import (Blueprint, flash, redirect, render_template, request,
                   send_from_directory, url_for, jsonify, make_response)

from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot
# from opsoro.stoppable_thread import StoppableThread
from opsoro.sound import Sound


try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def constrain(n, minn, maxn): return max(min(maxn, n), minn)

# from opsoro.expression import Expression

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

config = {
    'full_name':            'Blacklist',
    'author':               'howest',
    'icon':                 'fa-ban',
    'color':                'gray_dark',
    'difficulty':           4,
    'tags':                 [''],
    'allowed_background':   False,
    'multi_user':           True,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')

def setup_pages(opsoroapp):
    Blacklist_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    @Blacklist_bp.route('/', methods=['GET'])
    @opsoroapp.app_view
    def index():
        data = {'actions': {}}

        action = request.args.get('action', None)
        if action != None:
            data['actions'][action] = request.args.get('param', None)

        getBlacklistJson()
        text = "fuck fck f*ck ass a$$ cufk @ss"
        scanSwearWordsInText(text)

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    @Blacklist_bp.route('/signblacklist', methods=['POST'])
    def signblacklist():

        data = {'banlist': {}}
        bans = json.loads(request.form['banlist'])

        data['banlist'] = bans

        filename = os.path.join(Blacklist_bp.static_folder, 'blacklist.json')
        with open(filename, 'w') as blacklist_file:
                blacklist_file.write(json.dumps(data))

        getblacklist()

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)
        #return redirect("/")

    @Blacklist_bp.route('/getblacklist', methods=['GET'])
    def getblacklist():

        return jsonify(json.loads(getBlacklistJson()))


    def getBlacklistJson():
        if os.path.exists(os.path.join(Blacklist_bp.static_folder, 'blacklist.json')):
            filename = os.path.join(Blacklist_bp.static_folder, 'blacklist.json')
            with open(filename, 'r') as blacklist_file:
                try:
                    json_data = json.load(blacklist_file)
                except:
                    print_info("File is empty")
                    json_data = "{}"

                #print (json_data)
            return json.dumps(json_data)
        print_info("File doesn't exist")
        return '{}'

    def scanSwearWordsInText(text):

        regexList = SwearWordsToRegex()

        for word in regexList:

            #regex = ur"" + word
            print_info ( word )
            regex = ur"[F,f]*[*,$,@,!,.,0,1,3]*[U,u]*[*,$,@,!,.,0,1,3]*[C,c]*[*,$,@,!,.,0,1,3]*[K,k]*[*,$,@,!,.,0,1,3]*"
            print_info (re.compile(ur, word))
            #for swearWordRegex in regex:

            matches = re.finditer(regex, text)
            for matchNum, match in enumerate(matches):
                matchNum = matchNum + 1

                # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

                for groupNum in range(0, len(match.groups())):
                    groupNum = groupNum + 1

                    # print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))


        # Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.

        return;

    def SwearWordsToRegex():

        regex = []
        regexwords = []
        blacklistJSON = json.loads(getBlacklistJson())
        symbols = "[*,$,@,!,.,0,1,3]*"

        for word in blacklistJSON['banlist']:

            swaerWord = word['banWord']
            splittedSwarWord =  list(swaerWord)
            regixwoord = ""

            for letter in splittedSwarWord:

                letterUp = letter.upper()
                letterlow = letter.lower()
                regixletter = "["+ letterUp + "," + letterlow + "]*"+ symbols
                regixwoord = regixwoord + regixletter
                
                # 1e [F,f]*[*,$,@,!,.,0,1,3]*[U,u]*[*,$,@,!,.,0,1,3]*[C,c]*[*,$,@,!,.,0,1,3]*[K,k]*[*,$,@,!,.,0,1,3]*
                # 2e [(F,f)|(*,$,@,!,.,0,1,3)]*[(U,u)|(*,$,@,!,.,0,1,3)]*[(C,c)|(*,$,@,!,.,0,1,3)]*[(K,k)|(*,$,@,!,.,0,1,3)]*

            regex.append(regixwoord)

        return regex

    opsoroapp.register_app_blueprint(Blacklist_bp)

def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
