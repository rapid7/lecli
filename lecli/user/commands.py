"""
Module for user commands
"""
import click

from lecli.user import api


@click.command()
def get_users():
    """Get list of users in account"""
    api.list_users()


@click.command()
@click.option('-f', '--first', type=click.STRING,
              help='First name of user to be added')
@click.option('-l', '--last', type=click.STRING,
              help='Last name of user to be added')
@click.option('-e', '--email', type=click.STRING,
              help='Email address of user to be added')
@click.option('-u', '--userkey', type=click.STRING,
              help='User Key of user to be added')
@click.option('--force', is_flag=True,
              help='Force adding user with confirmation prompt')
def create_user(first, last, email, userkey, force):
    """Create a user on this account"""

    if not any((first, last, email, userkey)) or all((first, last, email, userkey)):
        click.echo('Example usage\n' +
                   'Add a new user: lecli create user -f John -l Smith -e john.smith@email.com\n' +
                   'Add an existing user: lecli create user -u 1343423')

    elif first and last and email is not None:
        if force:
            api.add_new_user(first, last, email)
        else:
            if click.confirm('Please confirm you want to add user ' + first + ' ' + last):
                api.add_new_user(first, last, email)

    elif userkey is not None:
        if force:
            api.add_existing_user(userkey)
        else:
            if click.confirm('Please confirm you want to add user with User Key ' + userkey):
                api.add_existing_user(userkey)


@click.command()
@click.option('-u', '--userkey', type=click.STRING,
              help='User Key of user to be deleted')
def delete_user(userkey):
    """Remove a user from this account and delete it.
    If the user is associated with other accounts,
    it will be removed from this account but not delete."""
    if userkey is None:
        click.echo('Example usage: lecli delete user -u 12345678-aaaa-bbbb-1234-1234cb123456')

    else:
        api.delete_user(userkey)


@click.command()
def get_owner():
    """Get account owner details"""
    api.get_owner()
