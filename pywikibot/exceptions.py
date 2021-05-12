"""**Pywikibot Exceptions** and warning classes.

This module contains all exception and warning classes used throughout
the framework::

    Exception
     +-- Error
          +-- APIError
          |    +-- APIMWError
          |    +-- UploadError
          +-- AutoblockUserError
          +-- CaptchaError
          +-- InvalidTitleError
          +-- NoUsernameError
          +-- PageInUseError
          +-- PageRelatedError
          |    +-- CircularRedirectError
          |    +-- InterwikiRedirectPageError
          |    +-- IsNotRedirectPageError
          |    +-- IsRedirectPageError
          |    +-- NoMoveTargetError
          |    +-- NoPageError
          |    +-- NotEmailableError
          |    +-- PageLoadRelatedError
          |    |    +-- InconsistentTitleError
          |    |    +-- InvalidPageError
          |    +-- PageSaveRelatedError
          |    |    +-- EditConflictError
          |    |    |    +-- ArticleExistsConflictError
          |    |    |    +-- PageCreatedConflictError
          |    |    |    +-- PageDeletedConflictError
          |    |    +-- LockedPageError
          |    |    |    +-- LockedNoPageError
          |    |    |    +-- CascadeLockedPageError
          |    |    +-- NoCreateError
          |    |    +-- OtherPageSaveError
          |    |    +-- SpamblacklistError
          |    |    +-- TitleblacklistError
          |    |    +-- AbuseFilterDisallowedError
          |    +-- UnsupportedPageError
          +-- SectionError
          +-- ServerError
          |    +-- FatalServerError
          |    +-- Server414Error
          |    +-- Server504Error
          +-- SiteDefinitionError
          |    +-- UnknownFamilyError
          |    +-- UnknownSiteError
          +-- TimeoutError
          |    +-- MaxlagTimeoutError
          +-- TranslationError
          +-- UserRightsError
          |    +-- HiddenKeyError (KeyError)
          +-- UnhandledAnswerError
          +-- UnknownExtensionError (NotImplementedError)
          +-- VersionParseError
          +-- WikiBaseError
               +-- CoordinateGlobeUnknownError (NotImplementedError)
               +-- EntityTypeUnknownError
               +-- NoWikibaseEntityError

    UserWarning
     +-- ArgumentDeprecationWarning (FutureWarning)
     +-- FamilyMaintenanceWarning

    RuntimeWarning
     +-- NotImplementedWarning


Error: Base class, all exceptions should the subclass of this class.

  - NoUsernameError: Username is not in user-config.py, or it is invalid.
  - AutoblockUserError: requested action on a virtual autoblock user not valid
  - TranslationError: no language translation found
  - UserRightsError: insufficient rights for requested action
  - InvalidTitleError: Invalid page title
  - CaptchaError: Captcha is asked and config.solve_captcha == False
  - i18n.TranslationError: i18n/l10n message not available
  - PageInUseError: Page cannot be reserved due to a lock
  - UnhandledAnswerError: bot choice caused a problem to arise
  - UnknownExtensionError: Extension is not defined for this site
  - VersionParseError: failed to parse version information
  - SectionError: The section specified by # does not exist

APIError: wiki API returned an error

  - APIMWError: MediaWiki internal exception
  - UploadError: upload failed

SiteDefinitionError: Site loading problem

  - UnknownSiteError: Site does not exist in Family
  - UnknownFamilyError: Family is not registered

PageRelatedError: any exception which is caused by an operation on a Page.

  - NoPageError: Page does not exist
  - UnsupportedPageError: Page is not supported due to a namespace restriction
  - IsRedirectPageError: Page is a redirect page
  - IsNotRedirectPageError: Page is not a redirect page
  - CircularRedirectError: Page is a circular redirect
  - InterwikiRedirectPageError: Page is a redirect to another site
  - InvalidPageError: Page is invalid e.g. without history
  - NotEmailableError: The target user has disabled email
  - NoMoveTargetError: An expected move target page does not exist

PageLoadRelatedError: any exception which happens while loading a Page.
  - InconsistentTitleError: Page receives a title inconsistent with query

PageSaveRelatedError: page exceptions within the save operation on a Page

  - AbuseFilterDisallowedError: AbuseFilter disallowed
  - SpamblacklistError: MediaWiki spam filter detected a blacklisted URL
  - TitleblacklistError: MediaWiki detected a blacklisted page title
  - OtherPageSaveError: misc. other save related exception.
  - LockedPageError: Page is locked
      - LockedNoPageError: Title is locked against creation
      - CascadeLockedPageError: Page is locked due to cascading protection
  - EditConflictError: Edit conflict while uploading the page
      - PageDeletedConflictError: Page was deleted since being retrieved
      - PageCreatedConflictError: Page was created by another user
      - ArticleExistsConflictError: Page article already exists
  - NoCreateError: parameter nocreate not allow page creation

ServerError: a problem with the server.

  - FatalServerError: A fatal/non-recoverable server error
  - Server414Error: Server timed out with HTTP 414 code
  - Server504Error: Server timed out with HTTP 504 code

WikiBaseError: any issue specific to Wikibase.

  - NoWikibaseEntityError: entity doesn't exist
  - CoordinateGlobeUnknownError: globe is not implemented yet.
  - EntityTypeUnknownError: entity type is not available on the site.

TimeoutError: request failed with a timeout

  - MaxlagTimeoutError: request failed with a maxlag timeout

DeprecationWarning: old functionality replaced by new functionality

PendingDeprecationWarning: problematic code which has not yet been
fully deprecated, possibly because a replacement is not available

RuntimeWarning: problems developers should have fixed, and users need to
be aware of its status.

  - tools._NotImplementedWarning: do not use
  - NotImplementedWarning: functionality not implemented

UserWarning: warnings targeted at users

  - config._ConfigurationDeprecationWarning: user configuration file problems
  - login._PasswordFileWarning: password file problems
  - ArgumentDeprecationWarning: command line argument problems
  - FamilyMaintenanceWarning: missing information in family definition

*Changed in version 6.0:* exceptions were renamed and are ending with "Error".
"""
#
# (C) Pywikibot team, 2008-2021
#
# Distributed under the terms of the MIT license.
#
import re
import sys
from typing import Optional, Union

from pywikibot.tools import (
    ModuleDeprecationWrapper,
    _NotImplementedWarning,
    issue_deprecation_warning,
)


class NotImplementedWarning(_NotImplementedWarning):

    """Feature that is no longer implemented."""


class ArgumentDeprecationWarning(UserWarning, FutureWarning):

    """Command line argument that is no longer supported."""


class FamilyMaintenanceWarning(UserWarning):

    """Family class is missing definitions."""


class Error(Exception):

    """Pywikibot error."""

    def __init__(self, arg: str):
        """Initializer."""
        self.unicode = arg

    def __str__(self) -> str:
        """Return a string representation."""
        return self.unicode


class APIError(Error):

    """The wiki site returned an error message."""

    def __init__(self, code, info, **kwargs):
        """Save error dict returned by MW API."""
        self.code = code
        self.info = info
        self.other = kwargs
        self.unicode = self.__str__()

    def __repr__(self):
        """Return internal representation."""
        return '{name}("{code}", "{info}", {other})'.format(
            name=self.__class__.__name__, **self.__dict__)

    def __str__(self):
        """Return a string representation."""
        if self.other:
            return '{}: {}\n[{}]'.format(
                self.code,
                self.info,
                ';\n '.join(
                    '{}: {}'.format(key, val)
                    for key, val in self.other.items()))

        return '{}: {}'.format(self.code, self.info)


class APIMWError(APIError):

    """The API site returned an error about a MediaWiki internal exception."""

    def __init__(self, mediawiki_exception_class_name, info, **kwargs):
        """Save error dict returned by MW API."""
        self.mediawiki_exception_class_name = mediawiki_exception_class_name
        code = 'internal_api_error_' + mediawiki_exception_class_name
        super().__init__(code, info, **kwargs)


class UploadError(APIError):

    """Upload failed with a warning message (passed as the argument)."""

    def __init__(self, code, message,
                 file_key: Optional[str] = None,
                 offset: Union[int, bool] = 0):
        """
        Create a new UploadError instance.

        @param file_key: The file_key of the uploaded file to reuse it later.
            If no key is known or it is an incomplete file it may be None.
        @param offset: The starting offset for a chunked upload. Is False when
            there is no offset.
        """
        super().__init__(code, message)
        self.file_key = file_key
        self.offset = offset

    @property
    def message(self):
        """Return warning message."""
        return self.info


class PageRelatedError(Error):

    """
    Abstract Exception, used when the exception concerns a particular Page.

    This class should be used when the Exception concerns a particular
    Page, and when a generic message can be written once for all.
    """

    # Preformatted message where the page title will be inserted.
    # Override this in subclasses.
    message = ''

    def __init__(self, page, message: Optional[str] = None):
        """
        Initializer.

        @param page: Page that caused the exception
        @type page: Page object
        """
        if message:
            self.message = message

        if self.message is None:
            raise Error("PageRelatedError is abstract. Can't instantiate it!")

        self.page = page
        self.title = page.title(as_link=True)
        self.site = page.site

        if re.search(r'\{\w+\}', self.message):
            msg = self.message.format_map(self.__dict__)
        elif re.search(r'%\(\w+\)s', self.message):
            issue_deprecation_warning("'%' style messages are deprecated, "
                                      'please use str.format() style instead',
                                      since='20210504',
                                      warning_class=FutureWarning)
            msg = self.message % self.__dict__
        elif '%s' in self.message:
            msg = self.message % page
        else:
            msg = self.message.format(page)

        super().__init__(msg)


class PageSaveRelatedError(PageRelatedError):

    """Saving the page has failed."""

    message = 'Page {} was not saved.'


class OtherPageSaveError(PageSaveRelatedError):

    """Saving the page has failed due to uncatchable error."""

    message = 'Edit to page {title} failed:\n{reason}'

    def __init__(self, page, reason: Union[str, Exception]):
        """Initializer.

        @param reason: Details of the problem
        """
        self.reason = reason
        super().__init__(page)

    @property
    def args(self):
        """Expose args."""
        return str(self.reason)


class NoUsernameError(Error):

    """Username is not in user-config.py."""


class NoPageError(PageRelatedError):

    """Page does not exist."""

    message = "Page {} doesn't exist."


class UnsupportedPageError(PageRelatedError):

    """Unsupported page due to namespace restriction."""

    # namespaces < 0 aren't supported (T169213)
    message = 'Page {} is not supported due to namespace restriction.'


class NoMoveTargetError(PageRelatedError):

    """Expected move target page not found."""

    message = 'Move target page of {} not found.'


class PageLoadRelatedError(PageRelatedError):

    """Loading the contents of a Page object has failed."""

    message = 'Page {} was not loaded.'


class InconsistentTitleError(PageLoadRelatedError):

    """Page receives a title inconsistent with query."""

    def __init__(self, page, actual: str):
        """Initializer.

        @param page: Page that caused the exception
        @type page: Page object
        @param actual: title obtained by query

        """
        self.message = "Query on {{}} returned data on '{}'".format(actual)
        super().__init__(page)


class SiteDefinitionError(Error):

    """Site does not exist."""


class UnknownSiteError(SiteDefinitionError):

    """Site does not exist in Family."""


class UnknownFamilyError(SiteDefinitionError):

    """Family is not registered."""


class UnknownExtensionError(Error, NotImplementedError):

    """Extension is not defined."""


class VersionParseError(Error):

    """Failed to parse version information."""


class IsRedirectPageError(PageRelatedError):

    """Page is a redirect page."""

    message = 'Page {} is a redirect page.'


class IsNotRedirectPageError(PageRelatedError):

    """Page is not a redirect page."""

    message = 'Page {} is not a redirect page.'


class CircularRedirectError(PageRelatedError):

    """Page is a circular redirect.

    Exception argument is the redirect target; this may be the same title
    as this page or a different title (in which case the target page directly
    or indirectly redirects back to this one)

    """

    message = 'Page {} is a circular redirect.'


class InterwikiRedirectPageError(PageRelatedError):

    """
    Page is a redirect to another site.

    This is considered invalid in Pywikibot. See bug T75184.

    """

    message = ('Page redirects to a page on another Site.\n'
               'Page: {page}\n'
               'Target page: {target_page} on {target_site}.')

    def __init__(self, page, target_page):
        """Initializer.

        @param target_page: Target page of the redirect.
        @type target_page: Page
        """
        self.target_page = target_page
        self.target_site = target_page.site
        super().__init__(page)


class InvalidPageError(PageLoadRelatedError):

    """Missing page history.

    *New in version 6.2.*
    """

    message = 'Page %s is invalid.'


class InvalidTitleError(Error):

    """Invalid page title."""


class LockedPageError(PageSaveRelatedError):

    """Page is locked."""

    message = 'Page {} is locked.'


class LockedNoPageError(LockedPageError):

    """Title is locked against creation."""

    message = 'Page {} does not exist and is locked preventing creation.'


class CascadeLockedPageError(LockedPageError):

    """Page is locked due to cascading protection."""

    message = 'Page {} is locked due to cascading protection.'


class SectionError(Error):

    """The section specified by # does not exist."""

    pass


class NoCreateError(PageSaveRelatedError):

    """Parameter nocreate doesn't allow page creation."""

    message = 'Page {} could not be created due to parameter nocreate'


class EditConflictError(PageSaveRelatedError):

    """There has been an edit conflict while uploading the page."""

    message = 'Page {} could not be saved due to an edit conflict'


class PageDeletedConflictError(EditConflictError):

    """Page was deleted since being retrieved."""

    message = 'Page {} has been deleted since last retrieved.'


class PageCreatedConflictError(EditConflictError):

    """Page was created by another user."""

    message = 'Page {} has been created since last retrieved.'


class ArticleExistsConflictError(EditConflictError):

    """Page already exists."""

    message = ('Destination article {} already exists and is not a redirect '
               'to the source article')


class AbuseFilterDisallowedError(PageSaveRelatedError):

    """Page save failed because the AbuseFilter disallowed it."""

    message = ('Edit to page %(title)s disallowed by the AbuseFilter.\n'
               '%(info)s\n%(warning)s')

    def __init__(self, page, info, warning):
        """Initializer."""
        self.info = info
        self.warning = warning
        super().__init__(page)


class SpamblacklistError(PageSaveRelatedError):

    """Page save failed because MediaWiki detected a blacklisted spam URL."""

    message = ('Edit to page {title} rejected by spam filter due to '
               'content:\n{url}')

    def __init__(self, page, url):
        """Initializer."""
        self.url = url
        super().__init__(page)


class TitleblacklistError(PageSaveRelatedError):

    """Page save failed because MediaWiki detected a blacklisted page title."""

    message = 'Page {} is title-blacklisted.'


class ServerError(Error):

    """Got unexpected server response."""


class FatalServerError(ServerError):

    """A fatal server error will not be corrected by resending the request."""


class Server504Error(ServerError):

    """Server timed out with HTTP 504 code."""


class Server414Error(ServerError):

    """Server returned with HTTP 414 code."""


class CaptchaError(Error):

    """Captcha is asked and config.solve_captcha == False."""


class AutoblockUserError(Error):

    """Requested action on a virtual autoblock user not valid.

    The class AutoblockUserError is an exception that is raised whenever
    an action is requested on a virtual autoblock user that's not available
    for him (i.e. roughly everything except unblock).
    """


class UnhandledAnswerError(Error):

    """The given answer didn't suffice."""

    def __init__(self, stop=False):
        """Initializer."""
        self.stop = stop


class TranslationError(Error, ImportError):

    """Raised when no correct translation could be found.

    Inherits from ImportError, as this exception is now used
    where previously an ImportError would have been raised,
    and may have been caught by scripts as such.
    """


class UserRightsError(Error):

    """Insufficient user rights to perform an action."""


class HiddenKeyError(UserRightsError, KeyError):

    """Insufficient user rights to view the hidden key."""


class NotEmailableError(PageRelatedError):

    """This user is not emailable."""

    message = '{} is not emailable.'


class PageInUseError(Error):

    """Page cannot be reserved for writing due to existing lock."""


class WikiBaseError(Error):

    """Wikibase related error."""


class NoWikibaseEntityError(WikiBaseError):

    """This entity doesn't exist."""

    def __init__(self, entity):
        """
        Initializer.

        @param entity: Wikibase entity
        @type entity: WikibaseEntity
        """
        super().__init__("Entity '{}' doesn't exist on {}"
                         .format(entity.id, entity.repo))
        self.entity = entity


class CoordinateGlobeUnknownError(WikiBaseError, NotImplementedError):

    """This globe is not implemented yet in either WikiBase or pywikibot."""


class EntityTypeUnknownError(WikiBaseError):

    """The requested entity type is not recognised on this site."""


class TimeoutError(Error):

    """Request failed with a timeout error."""


class MaxlagTimeoutError(TimeoutError):

    """Request failed with a maxlag timeout error."""


DEPRECATED_EXCEPTIONS = {
    'NoUsername': 'NoUsernameError',
    'NoPage': 'NoPageError',
    'UnsupportedPage': 'UnsupportedPageError',
    'NoMoveTarget': 'NoMoveTargetError',
    'InconsistentTitleReceived': 'InconsistentTitleError',
    'UnknownSite': 'UnknownSiteError',
    'UnknownFamily': 'UnknownFamilyError',
    'UnknownExtension': 'UnknownExtensionError',
    'IsRedirectPage': 'IsRedirectPageError',
    'IsNotRedirectPage': 'IsNotRedirectPageError',
    'CircularRedirect': 'CircularRedirectError',
    'InterwikiRedirectPage': 'InterwikiRedirectPageError',
    'InvalidTitle': 'InvalidTitleError',
    'LockedPage': 'LockedPageError',
    'LockedNoPage': 'LockedNoPageError',
    'CascadeLockedPage': 'CascadeLockedPageError',
    'EditConflict': 'EditConflictError',
    'PageDeletedConflict': 'PageDeletedConflictError',
    'PageCreatedConflict': 'PageCreatedConflictError',
    'ArticleExistsConflict': 'ArticleExistsConflictError',
    'AutoblockUser': 'AutoblockUserError',
    'NoWikibaseEntity': 'NoWikibaseEntityError',
    'CoordinateGlobeUnknownException': 'CoordinateGlobeUnknownError',
    'EntityTypeUnknownException': 'EntityTypeUnknownError',
}

wrapper = ModuleDeprecationWrapper(__name__)
module = sys.modules[__name__]

for old_name, new_name in DEPRECATED_EXCEPTIONS.items():
    setattr(module, old_name, getattr(module, new_name))
    wrapper._add_deprecated_attr(old_name, replacement_name=new_name,
                                 since='20210423', future_warning=True)
