import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

def create_blueprint(identificator : str, prefix : str) : 
    return Blueprint(identificator, __name__, url_prefix = prefix)