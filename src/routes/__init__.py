from .review_route import blueprint_review
from .blacklist_route import blueprint_blacklist
from .fbusers_route import blueprint_fbusers
from .client import blueprint_clients

# Novos imports para geracao e verificacao de codigos TOTP usando Google Authenticator
from .generate import bp_generate
from .verify import bp_verify


__all__ = ["blueprint_review", "blueprint_blacklist", "blueprint_fbusers", "blueprint_clients", "bp_generate", "bp_verify"]
