# Setup Python path
import sys, setup
import definitions as defs
sys.path.append("..")


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi
from cortex_client.api.collection import ResourceNotFoundException


#==============================================================================
# Script

def delete_resources():
    # API from server cortex listening on port 8000 of localhost is used
    # Username "admin" and password "secret" are used for authentification
    api = CortexApi(setup.global_vars.comodit_url, setup.global_vars.comodit_user, setup.global_vars.comodit_pass)

    org_coll = api.organizations()
    hosts = []
    plats = []
    apps = []
    dists = []
    try:
        org = org_coll.get_resource(setup.global_vars.org_name)

        app_coll = org.applications()
        for name in setup.global_vars.app_names:
            try:
                apps.append(app_coll.get_resource(name))
            except ResourceNotFoundException:
                print "Application", name, "does not exist"

        plat_coll = org.platforms()
        for name in setup.global_vars.plat_names:
            try:
                plats.append(plat_coll.get_resource(name))
            except ResourceNotFoundException:
                print "Platform does not exist"

        dist_coll = org.distributions()
        for name in setup.global_vars.dist_names:
            try:
                dists.append(dist_coll.get_resource(name))
            except ResourceNotFoundException:
                print "Distribution does not exist"

        env_coll = org.environments()
        try:
            env = env_coll.get_resource(setup.global_vars.env_name)

            host_coll = env.hosts()
            for plat_name in setup.global_vars.plat_names:
                try:
                    hosts.append(host_coll.get_resource(defs.get_host_name(plat_name)))
                except ResourceNotFoundException:
                    print "Host does not exist"
        except ResourceNotFoundException:
            print "Environment does not exist"
    except ResourceNotFoundException:
        print "Organization does not exist"


    ###################
    # Delete entities #
    ###################

    print "="*80
    print "Delete hosts"
    for host in hosts:
        try:
            host.instance().get_single_resource().poweroff()
        except:
            pass

        try:
            host.instance().get_single_resource().delete()
        except Exception, e:
            print e.message

        try:
            host.delete()
        except Exception, e:
            print e.message

    print "="*80
    print "Delete applications"
    try:
        for app in apps:
            try:
                app.delete()
            except Exception, e:
                print e.message
    except Exception, e:
        print e.message

    print "="*80
    print "Delete platform"
    try:
        for plat in plats:
            try:
                plat.delete()
            except Exception, e:
                print e.message
    except Exception, e:
        print e.message

    print "="*80
    print "Delete distribution"
    try:
        for dist in dists:
            try:
                dist.delete()
            except Exception, e:
                print e.message
    except Exception, e:
        print e.message

    print "="*80
    print "Delete environments"
    try:
        env.delete()
    except Exception, e:
        print e.message

    print "="*80
    print "Delete organization"
    try:
        org.delete()
    except Exception, e:
        print e.message


#==============================================================================
# Entry point
if __name__ == "__main__":
    setup.setup()
    defs.define()
    delete_resources()
