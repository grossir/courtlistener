# This software and any associated files are copyright 2010 Brian Carver and
# Michael Lissner.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import settings
from django.core.management import setup_environ
setup_environ(settings)

from userHandling.models import UserProfile
from django.contrib.sites.models import Site
from django.core.mail import send_mail

import datetime
import hashlib
import random
from optparse import OptionParser


def delete_old_accounts(verbose, simulate):
    """This script will find accounts older than roughly two months that have
    not been confirmed, and delete them. It can be run once a month, or so.
    """

    two_months_ago = (datetime.date.today() - datetime.timedelta(60))

    # get the accounts
    unconfirmed_ups = UserProfile.objects.filter(emailConfirmed = False,
        key_expires__lte = two_months_ago.isoformat())

    for up in unconfirmed_ups:
        if verbose:
            print "User \"" + up.user.username + "\" deleted."

        if not simulate:
            # Gather their foreign keys, delete those, then delete their
            # profile and user info
            alerts = up.alert.all()
            for alert in alerts:
                alert.delete()

            # delete the user then the profile.
            up.user.delete()
            up.delete()

    return 0


def notify_unconfirmed(verbose, simulate):
    """This function will notify people who have not confirmed their accounts
    that they must do so for fear of the deletion bots (above). This function
    should be run once a week, or so."""

    # if your account is more than a week old, and you have not confirmed it,
    # we will send you a notification, requesting that you confirm it.
    a_week_ago = (datetime.date.today() - datetime.timedelta(7))

    # get the accounts
    unconfirmed_ups = UserProfile.objects.filter(emailConfirmed = False,
        key_expires__lte = a_week_ago)

    for up in unconfirmed_ups:
        if verbose:
            print "User \"" + up.user.username + "\" will be notified."
        if not simulate:
            user = up.user
            # Build and save a new activation key for the account.
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activationKey = hashlib.sha1(salt+user.username).hexdigest()
            up.activationKey = activationKey
            up.save()

            # Send the email.
            current_site = Site.objects.get_current()
            email_subject = 'Please confirm your account on ' + \
                current_site.name,
            email_body = "Hello, %s,\n\nDuring routine maintenance of our \
site, we discovered that your email address has not yet been confirmed. \
To confirm your email address and continue using our site, please click the \
following link:\n\nhttp://courtlistener.com/email/confirm/%s\n\n\
Unfortuantely, accounts that are not confirmed will stop receiving alerts, \
and must eventually be deleted from our system.\n\n\
Thanks for using our site,\n\nThe CourtListener team\n\n\
-------------------\nFor questions or comments, please see our contact page, \
http://courtlistener.com/contact/." % (
                user.username,
                up.activationKey)
            send_mail(email_subject,
                      email_body,
                      'no-reply@courtlistener.com',
                      [user.email])
    return 0


def find_legit():
    # find accounts that have alerts, and mark them as confirmed.
    # this is a one-off script used to grandfather-in old accounts
    real_users = UserProfile.objects.filter(emailConfirmed = False)

    for user in real_users:
        if user.alert.count() > 0:
            print "User \"" + user.user.username + \
                "\" is toggled to confirmed."
            user.emailConfirmed = True
            user.save()

    return 0


def main():
    usage = "usage: %prog [--verbose] [--simulate]"
    parser = OptionParser(usage)
    parser.add_option('-g', '--grandfather', action='store_true',
        dest='grandfather', default=False, help="Grandfather in legit users.")
    parser.add_option('-n', '--notify', action="store_true", dest='notify',
        default=False, help="Notify users with unconfirmed accounts older " +\
        "five days.")
    parser.add_option('-d', '--delete', action="store_true", dest='delete',
        default=False, help="Delete unconfirmed accounts older than two " +\
        "months.")
    parser.add_option('-v', '--verbose', action="store_true", dest='verbose',
        default=False, help="Display variable values during execution")
    parser.add_option('-s', '--simulate', action="store_true",
        dest='simulate', default=False, help="Simulate the emails that " + \
        "would be sent, using the console backend. Do not delete accounts.")
    (options, args) = parser.parse_args()

    verbose = options.verbose
    simulate = options.simulate
    delete = options.delete
    notify = options.notify
    grandfather = options.grandfather

    if grandfather:
        find_legit()
    if delete:
        delete_old_accounts(verbose, simulate)
    if notify:
        notify_unconfirmed(verbose, simulate)
    if simulate:
        print "******************************************"
        print "* NO EMAILS SENT OR ACCOUNTS DEACTIVATED *"
        print "******************************************"

    return 0


if __name__ == '__main__':
    main()
