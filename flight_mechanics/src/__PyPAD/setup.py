# http://learnpythonthehardway.org/book/ex46.html

def main():
    
    from distutils.core import setup

    # list all SUAVE sub packages
    print('Listing Packages and Sub-Packages:')
    packages = list_subpackages('PyPAD',verbose=True)
    packages = map( '.'.join, packages )
    
    setup(name='Distutils',
          version='1.0',
          description='Python Distribution Utilities',
          author='Greg Ward',
          author_email='gward@python.net',
          url='https://www.python.org/sigs/distutils-sig/',
          packages=packages
         )    
	
    return
    
# ----------------------------------------------------------------------
#   Helper Functions
# ----------------------------------------------------------------------
	
def list_subpackages(package_trail,verbose=False):
    """ package_trails = list_subpackages(package_trail)
        returns a list of package trails

        Inputs: 
            package_trail : a list of dependant package names, as strings
            example: os.path -> ['os','path']

        Outputs:
            package_trails : a list of package trails
            can be processed with >>> map( '.'.join, package_trails )
    """
        
    # imports
    import os

    # error checking
    if isinstance(package_trail,str):
        package_trail = [package_trail]
    elif not isinstance(package_trail,(list,tuple)):
        raise(Exception , '%s is not iterable' % package)

    # print current package
    if verbose:
        print('.'.join(package_trail))

    # get absolute path for package
    package_dir = os.path.abspath( os.path.join(*package_trail) )

    # find all packages
    packages = [ 
        p for p in os.listdir( package_dir ) \
        if ( os.path.isdir(os.path.join(package_dir, p)) and              # package is a directory
             os.path.isfile(os.path.join(package_dir, p, '__init__.py')) ) # and has __init__.py
    ]

    # append package trail
    packages = [ package_trail + [p] for p in packages ]

    # recursion, check for sub packages
    packages = [ subpackage \
                 for package in packages \
                 for subpackage in list_subpackages(package,verbose) ]

    # include this package trail
    package_trails = [package_trail] + packages

    # done!
    return package_trails

# ----------------------------------------------------------------------
#   Call Main
# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
