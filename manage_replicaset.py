from os import path
from kubernetes import client, config
import yaml
import json

# Configs can be set in Configuration class directly or using helper utility

config  = client.Configuration()
config.api_key_prefix['authorization'] = "Bearer"
config.host = "https://192.168.56.101:6443"
config.api_key['authorization'] = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ilp6dWR3SDZPeDFlYV90NVY2UnAxVnFzR2YxT2s5bGZzUHRna3hMYzBGTjgifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiw
ia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tcXBqZzUiLCJrdWJlcm5ldGVzLmlv
L3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImViYmVhOWI1LWMzZjgtNGVkNS1iM2Y5LWM3ZDNlN
2Q2ODlkNiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.n23MZf0kSQX1Z2So57goUZvj0y2iQdabY1GvK_gXxeFvUJWsMMjhNDmJqS6LWCpjSx1Vy9-pGkKv6MM8fa4DGNY-8vGzhOWjSR0
wVwcmW8AWTUuFBAs_4IDHkW2VahzJ_nWj1XgXT6C_SVoKEwxltY3dEbHfcW_6_zZJhNaNMow8g6Xi10eZcYAaWxN16rqDQag8v_-4Lmbfx6kPAmra_72d9wCMC8kbuGqIdp6YH0u2GBFki0NAm64c4DXinVnGzJr9S8p4P2ob8con
gEeVmcgvRZ06tgkW3FspgztUrlfeanr_cz4dK2fiIKRRGVrjTNc5Iy2sGY468OHSwfnSYg"
config.verify_ssl = False

appclient  = client.ApiClient(config)
core_client = client.CoreV1Api(appclient)
api_client  = client.AppsV1Api(appclient)

def get_replicaset(arg_cli,arg_ns):

        try:
            ret_val =   arg_cli.list_namespaced_replication_controller(arg_ns)
        except ApiException as e:
            print("Exception when calling list_namespaced_replication_controller: %s\n" % e)

        print (ret_val)

        #for i in ret_val.items:
        #    print("%s\t%s\t" %(i.metadata.namespace,i.metadata.name))
#EndDef

def get_replicaset_scale(arg_cli,arg_ns,arg_rs):

        try:
            ret_val =   arg_cli.read_namespaced_replica_set_scale(arg_rs,arg_ns)
        except ApiException as e:
            print("Exception when calling list_namespaced_replication_controller: %s\n" % e)

        print(ret_val)
        print("ReplicaSet    Status " )
        print("%s\t\t%s\t" %(ret_val.spec.replicas,ret_val.status.replicas))

#EndDef

def set_replicaset_scale(arg_cli,arg_ns,arg_rs,arg_scale):
        mt_config               =   client.V1ObjectMeta()
        mt_config.name          =   arg_rs
        mt_config. namespace    =   arg_ns
        rs_config               =   client.V1ScaleSpec()
        rs_config.replicas      =   0
        s_config                =   client.V1Scale()
        s_config.api_version    =   'autoscaling/v1'
        s_config.kind           =   "Scale"
        s_config.spec           =   rs_config
        s_config.metadata       =   mt_config

        try:
            #ret_val = arg_cli.replace_namespaced_replica_set_scale(name=arg_rs, namespace=arg_ns, body=s_config)
            ret_val = arg_cli.patch_namespaced_replica_set_scale(name=arg_rs, namespace=arg_ns, body=s_config)
            #ret_val = arg_cli.replace_namespaced_replication_controller_scale(name=arg_rs, namespace=arg_ns, body=2)
            print(ret_val)
        except ApiException as e:
            print("Exception %s" % e )
#EndDef

def set_deployment_scale(arg_cli,arg_ns,arg_rs,arg_scale):
        mt_config               =   client.V1ObjectMeta()
        mt_config.name          =   arg_rs
        mt_config. namespace    =   arg_ns
        rs_config               =   client.V1ScaleSpec()
        rs_config.replicas      =   arg_scale
        s_config                =   client.V1Scale()
        s_config.api_version    =   'autoscaling/v1'
        s_config.kind           =   "Scale"
        s_config.spec           =   rs_config
        s_config.metadata       =   mt_config

        try:
            ret_val = arg_cli.replace_namespaced_deployment_scale(name=arg_rs, namespace=arg_ns, body=s_config)
            #ret_val = arg_cli.replace_namespaced_replication_controller_scale(name=arg_rs, namespace=arg_ns, body=2)
            print(ret_val)
        except ApiException as e:
            print("Exception %s" % e )
#EndDef


def get_deployment(arg_cli,arg_ns):
        try:
            ret_val =   arg_cli.list_namespaced_deployment(arg_ns)
        except ApiException as e:
            print("Exception Occured %s" %e)

        for i in ret_val.items:
            print("%s\t%s\t" %(i.metadata.namespace,i.metadata.name))

#EndDef

#get_replicaset(core_client,"default")
#get_deployment(api_client,"default")
#get_replicaset_scale(api_client,"default","nginx-7848d4b86f")
#set_replicaset_scale(api_client,"default","nginx-7848d4b86f",4)
set_deployment_scale(api_client,"default","nginx",3)
