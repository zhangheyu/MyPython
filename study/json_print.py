import json

json_data = '[{"ID":10,"Name":"Pankaj","Role":"CEO"},' \
            '{"ID":20,"Name":"David Lee","Role":"Editor"}]'

json_object = json.loads(json_data)

json_formatted_str = json.dumps(json_object, indent=2)

# print(json_formatted_str)


root = {}
path_dict = {
    "/": {
        "{{END}}": "/"
    },
    "/aa": {
        "{{END}}": "/aa",
        "/": {
            "{{END}}": "/aa/"
        }
    },
    "/bb": {
        "{{SUB_TREE}}": {
            "{{END}}": "/bb/*"
        },
        "{{END}}": "/bb"
    },
    "/cc": {
        "{{ANY}}": {
            "/profile": {
                "{{END}}": "/cc/{id}/profile"
            }
        },
        'cc': 'ccccccc'
    },
    "/cl": {
        "{{ANY}}": {
            "/profile": {
                "{{END}}": "/cl/{id}/profile"
            }
        },
        'cc': 'ccccc'
    }
}

for path, val in path_dict.items():
    # print('path:', path)
    # print('value:', val)

    if not path:
        assert False

    tree = path_dict

    if path.startswith('/c'):
        tree = val
    if 'cc' in tree:
        tree['cc'] = 'repeat'

# print(json.dumps(path_dict, indent=2))


result = dict(records='records', column_names='column_names',
              column_types='column_types')
# print(result)


upstreams = {
    "172.16.30.4_80": {
        "AIWaf_Modules": {
            "_value": {
                "aiwaf_enable": True,
                "aiwaf_learning_mode": True,
                "aiwaf_risk_model": {
                    "sql_inject_model": True,
                    "xss_inject_model": True
                },
                "aiwaf_whitelist": []
            }
        },
        "Accept_Encoding": {
            "_value": ""
        },
        "AjaxRequestBodyEncryptionList": {
            "_value": []
        },
        "AjaxResponseEncryptionList": {
            "_value": []
        },
        "ContentTypeOverwriteEntry": {
            "_value": []
        },
        "Enable_Attack_Sensation": {
            "_value": False
        },
        "Enable_Cookie_Collection": {
            "_value": False
        },
        "Enable_Post_Data_Collection": {
            "_value": False
        },
        "EncapsulationListOut": {
            "_value": []
        },
        "EntryPath": {
            "_value": "/"
        },
        "Extra_Business_Data": {
            "_value": [
                [
                    "login",
                    "/",
                    "admin",
                    "admin",
                    "",
                    "ok",
                    "1",
                    "off",
                    "1",
                    "",
                    "",
                    "",
                    "",
                    "",
                    True,
                    1,
                    "0",
                    False,
                    True,
                    128,
                    4096,
                    False,
                    "",
                    "",
                    False,
                    True,
                    0
                ]
            ]
        },
        "Extra_Session_in_Cookie": {
            "_value": ""
        },
        "FullWhiteList": {
            "_value": []
        },
        "FullWhiteListOut": {
            "_value": []
        },
        "Host": {
            "_value": "$http_host"
        },
        "Inject_Patternlist": {
            "_value": []
        },
        "Inject_Whitelist": {
            "_value": []
        },
        "IpBlackList": {
            "_value": []
        },
        "IpListSwitch": {
            "_value": "all_ip_white_list"
        },
        "IpWhiteList": {
            "_value": [
                [
                    "172.16.30.1",
                    "255.255.255.0",
                    "pc",
                    "segment"
                ]
            ]
        },
        "IsHttps": {
            "_value": False
        },
        "IsTerminalHttps": {
            "_value": False
        },
        "IsUpstreamHttps": {
            "_value": False
        },
        "ListenPort": {
            "_value": "80"
        },
        "MobileBlockWhiteList": {
            "_value": []
        },
        "MobileBodyVerificationList": {
            "_value": []
        },
        "MobileBodyWhiteList": {
            "_value": []
        },
        "MobileWhiteList": {
            "_value": []
        },
        "P3P_CP": {
            "_value": "NOI DSP PSAa OUR BUS IND ONL UNI COM NAV INT LOC"
        },
        "Request_Custom_Head_Key": {
            "_value": ""
        },
        "Request_Custom_Head_Value": {
            "_value": ""
        },
        "Response_Custom_Head_Key": {
            "_value": ""
        },
        "Response_Custom_Head_Mode": {
            "_value": "append"
        },
        "Response_Custom_Head_Value": {
            "_value": ""
        },
        "ServerName": {
            "_value": "172.16.30.4"
        },
        "ServerNameType": {
            "_value": "IPv4"
        },
        "TerminalEnabled": {
            "_value": False
        },
        "TerminalPort": {
            "_value": "80"
        },
        "UpstreamList": {
            "_value": [
                [
                    "65.61.137.117",
                    "80",
                    True
                ]
            ]
        },
        "VerificationList": {
            "_value": []
        },
        "WL_Proxy_Client_IP": {
            "_value": "$remote_addr"
        },
        "WafEnabledModules": {
            "_value": {
                "command_excute_interception": True,
                "file_upload_interception": True,
                "java_deserialization_interception": True,
                "local_file_include_interception": True,
                "php_injection_interception": True,
                "protocol_attack_interception": True,
                "remote_file_include_interception": True,
                "scanner_detect_interception": True,
                "sensitive_info_filter_interception": True,
                "server_vulnerability_interception": True,
                "session_fixation_interception": False,
                "sql_injection_interception": True,
                "web_shell_interception": False,
                "xss_injection_interception": True
            }
        },
        "Waf_Decodelist": {
            "_value": []
        },
        "X_Content_Type_Options": {
            "_value": "nosniff"
        },
        "X_Forwarded_For": {
            "_value": "$proxy_add_x_forwarded_for"
        },
        "X_Frame_Options": {
            "_value": "SAMEORIGIN"
        },
        "X_Real_IP": {
            "_value": "$remote_addr"
        },
        "X_XSS_Protection": {
            "_value": "1; mode=block"
        },
        "X_XSS_Protection_report_uri": {
            "_value": ""
        },
        "action": {
            "_value": "reject"
        },
        "ajax_referer_list": {
            "_value": []
        },
        "ajax_token_bypass_list": {
            "_value": []
        },
        "charset": {
            "_value": ""
        },
        "check_console_open": {
            "_value": False
        },
        "content_type_overwrite": {
            "_value": False
        },
        "disable_123456": {
            "_value": False
        },
        "disable_encoding_ajax_args": {
            "_value": False
        },
        "disable_upstream_keepalive": {
            "_value": True
        },
        "enableHttp2": {
            "_value": False
        },
        "enable_Accept_Encoding": {
            "_value": True
        },
        "enable_P3P_Options": {
            "_value": False
        },
        "enable_Request_Custom_Head": {
            "_value": False
        },
        "enable_Response_Custom_Head": {
            "_value": False
        },
        "enable_WL_Proxy_Client_IP": {
            "_value": False
        },
        "enable_X_Content_Type_Options": {
            "_value": False
        },
        "enable_X_Forwarded_For": {
            "_value": True
        },
        "enable_X_Real_IP": {
            "_value": True
        },
        "enable_X_XSS_Protection": {
            "_value": False
        },
        "enable_charset": {
            "_value": False
        },
        "enable_compatible_mode": {
            "_value": False
        },
        "enable_host": {
            "_value": False
        },
        "enable_http2https": {
            "_value": False
        },
        "enable_mobile_block_whitelist": {
            "_value": False
        },
        "enable_mobile_list": {
            "_value": False
        },
        "enable_mobile_protection": {
            "_value": False
        },
        "enable_webrtc": {
            "_value": False
        },
        "enable_x_frame_option": {
            "_value": False
        },
        "enabled": {
            "_value": True
        },
        "health_check": {
            "_value": {
                "health_check_interval": "10",
                "health_check_path": "/",
                "health_check_reset_times": "3",
                "health_check_timeouts": "5",
                "health_check_type": "http",
                "health_user_agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
                "is_health_check_enable": True
            }
        },
        "http2https_new_port": {
            "_value": "80"
        },
        "http2https_org_port": {
            "_value": "80"
        },
        "ie_rendering_mode": {
            "_value": False
        },
        "internal_res_path": {
            "_value": "/"
        },
        "keep_http_version": {
            "_value": False
        },
        "key": {
            "_value": "172.16.30.4_80"
        },
        "learning_mode": {
            "_value": False
        },
        "limit_except": {
            "_value": [
                True,
                True,
                False,
                False,
                False,
                True,
                False,
                False,
                False
            ]
        },
        "load_balancing_strategy": {
            "_value": "ip_hash"
        },
        "mobile_config_version": {
            "_value": 4
        },
        "mobile_customer_id": {
            "_value": "None"
        },
        "mobile_enable_ignore_jsonp": {
            "_value": False
        },
        "mobile_enable_online_perceptron": {
            "_value": False
        },
        "mobile_only": {
            "_value": False
        },
        "mobile_passthrough_collection": {
            "_value": False
        },
        "mobile_protect_rules": {
            "_value": ""
        },
        "mobile_v1_process_mode": {
            "_value": "block"
        },
        "name": {
            "_value": "172.16.30.4"
        },
        "no_content_type": {
            "_value": False
        },
        "prevent_corejs_reentry": {
            "_value": False
        },
        "prevent_scanner": {
            "_value": True
        },
        "protected_list": {
            "_value": {
                "aiwaf_attack_interception": True,
                "ajax_request_body_encryption": False,
                "ajax_response_encryption": False,
                "automated_tool_intercept": True,
                "crack_behavior_interception": True,
                "injection_attack_interception": True,
                "mobile_sdk_protection": False,
                "web_advanced_protection": False,
                "web_standard_protection": True
            }
        },
        "proxy_connect_timeout": {
            "_value": ""
        },
        "proxy_read_timeout": {
            "_value": ""
        },
        "proxy_send_timeout": {
            "_value": ""
        },
        "proxy_ssl_ciphers": {
            "_value": "DEFAULT"
        },
        "proxy_ssl_protocols": {
            "_value": "SSLv3, TLSv1, TLSv1.1, TLSv1.2"
        },
        "reduce_level_of_protection_by_ua": {
            "_value": False
        },
        "reload_status_code": {
            "_value": "412"
        },
        "reserve_comment": {
            "_value": True
        },
        "rule_set": {
            "_value": "customSet"
        },
        "scc": {
            "_value": {
                "enable": False,
                "text": ""
            }
        },
        "security_level_max": {
            "_value": [
                "bot",
                "cookie_token",
                "crack",
                "waf"
            ]
        },
        "security_level_min": {
            "_value": [
                "bot",
                "cookie_token",
                "crack",
                "waf"
            ]
        },
        "site_customize_name": {
            "_value": "testfire"
        },
        "src_ip_from": {
            "_value": ""
        },
        "src_ip_use_global_setting": {
            "_value": True
        },
        "ssl_ciphers": {
            "_value": "kEECDH:!RC4:!eNULL:!aNULL:!DES:DES-CBC3-SHA"
        },
        "ssl_protocols": {
            "_value": "TLSv1, TLSv1.1, TLSv1.2, TLSv1.3"
        },
        "static_resource_list": {
            "_value": "7z,aac,amr,asm,avi,bak,bat,bmp,bin,c,cab,css,csv,com,cpp,dat,dll,doc,dot,docx,exe,eot,fla,flc,fon,fot,font,gdb,gif,gz,gho,hlp,hpp,htc,ico,ini,inf,ins,iso,js,jar,jpg,jpeg,json,java,lib,log,map,mid,mp4,mpa,m4a,mp3,mpg,mkv,mod,mov,mim,mpp,msi,mpeg,obj,ocx,ogg,olb,ole,otf,py,pyc,pas,pgm,ppm,pps,ppt,pdf,pptx,png,pic,pli,psd,qif,qtx,ra,rm,ram,rmvb,reg,res,rtf,rar,so,sbl,sfx,swa,swf,svg,sys,tar,taz,tif,tiff,torrent,txt,ttf,vsd,vss,vsw,vxd,woff,woff2,wmv,wma,wav,wps,xbm,xpm,xls,xlsx,xsl,xml,z,zip,apk,plist,ipa"
        },
        "status": {
            "_value": "test_pass"
        },
        "test_output": {
            "_value": "nginx: the configuration file /etc/asp/release/nginx/nginx_t.conf syntax is ok<br/>nginx: configuration file /etc/asp/release/nginx/nginx_t.conf test is successful<br/>"
        },
        "useBuiltInCert": {
            "_value": False
        },
        "waf_add_disabled_set": {
            "_value": ""
        },
        "waf_custom_set_template": {
            "_value": "defaultSet"
        },
        "waf_del_disabled_set": {
            "_value": "960901,960902,960904,960905"
        },
        "waf_learning_mode": {
            "_value": True
        },
        "waf_rule_module_config": {
            "_value": {
                "sensitive_info_filter_interception": {
                    "action": "replace",
                    "skip_backend": 4,
                    "skip_forward": 3,
                    "target_name": "*"
                }
            }
        },
        "websocket_paths": {
            "_value": []
        },
        "x_frame_option_allow_uri": {
            "_value": ""
        },
        "xff_position": {
            "_value": "last"
        }
    },
    "172.16.30.4_8080": {
        "AIWaf_Modules": {
            "_value": {
                "aiwaf_enable": False,
                "aiwaf_learning_mode": False,
                "aiwaf_risk_model": {
                    "sql_inject_model": True,
                    "xss_inject_model": True
                },
                "aiwaf_whitelist": []
            }
        },
        "Accept_Encoding": {
            "_value": ""
        },
        "AjaxRequestBodyEncryptionList": {
            "_value": []
        },
        "AjaxResponseEncryptionList": {
            "_value": []
        },
        "ContentTypeOverwriteEntry": {
            "_value": []
        },
        "Enable_Attack_Sensation": {
            "_value": False
        },
        "Enable_Cookie_Collection": {
            "_value": False
        },
        "Enable_Post_Data_Collection": {
            "_value": False
        },
        "EncapsulationListOut": {
            "_value": []
        },
        "EntryPath": {
            "_value": "/"
        },
        "Extra_Business_Data": {
            "_value": []
        },
        "Extra_Session_in_Cookie": {
            "_value": ""
        },
        "FullWhiteList": {
            "_value": []
        },
        "FullWhiteListOut": {
            "_value": []
        },
        "Host": {
            "_value": "$http_host"
        },
        "Inject_Patternlist": {
            "_value": []
        },
        "Inject_Whitelist": {
            "_value": []
        },
        "IpBlackList": {
            "_value": []
        },
        "IpListSwitch": {
            "_value": "all_ip_white_list"
        },
        "IpWhiteList": {
            "_value": []
        },
        "IsHttps": {
            "_value": False
        },
        "IsTerminalHttps": {
            "_value": False
        },
        "IsUpstreamHttps": {
            "_value": False
        },
        "ListenPort": {
            "_value": "8080"
        },
        "MobileBlockWhiteList": {
            "_value": []
        },
        "MobileBodyVerificationList": {
            "_value": []
        },
        "MobileBodyWhiteList": {
            "_value": []
        },
        "MobileWhiteList": {
            "_value": []
        },
        "P3P_CP": {
            "_value": "NOI DSP PSAa OUR BUS IND ONL UNI COM NAV INT LOC"
        },
        "Request_Custom_Head_Key": {
            "_value": ""
        },
        "Request_Custom_Head_Value": {
            "_value": ""
        },
        "Response_Custom_Head_Key": {
            "_value": ""
        },
        "Response_Custom_Head_Mode": {
            "_value": "append"
        },
        "Response_Custom_Head_Value": {
            "_value": ""
        },
        "ServerName": {
            "_value": "172.16.30.4"
        },
        "ServerNameType": {
            "_value": "IPv4"
        },
        "TerminalEnabled": {
            "_value": False
        },
        "TerminalPort": {
            "_value": "80"
        },
        "UpstreamList": {
            "_value": [
                [
                    "10.10.65.20",
                    "80",
                    True
                ]
            ]
        },
        "VerificationList": {
            "_value": []
        },
        "WL_Proxy_Client_IP": {
            "_value": "$remote_addr"
        },
        "WafEnabledModules": {
            "_value": {
                "command_excute_interception": True,
                "file_upload_interception": False,
                "java_deserialization_interception": False,
                "local_file_include_interception": False,
                "php_injection_interception": False,
                "protocol_attack_interception": False,
                "remote_file_include_interception": False,
                "scanner_detect_interception": True,
                "sensitive_info_filter_interception": False,
                "server_vulnerability_interception": False,
                "session_fixation_interception": False,
                "sql_injection_interception": True,
                "web_shell_interception": False,
                "xss_injection_interception": True
            }
        },
        "Waf_Decodelist": {
            "_value": []
        },
        "X_Content_Type_Options": {
            "_value": "nosniff"
        },
        "X_Forwarded_For": {
            "_value": "$proxy_add_x_forwarded_for"
        },
        "X_Frame_Options": {
            "_value": "SAMEORIGIN"
        },
        "X_Real_IP": {
            "_value": "$remote_addr"
        },
        "X_XSS_Protection": {
            "_value": "1; mode=block"
        },
        "X_XSS_Protection_report_uri": {
            "_value": ""
        },
        "action": {
            "_value": "reject"
        },
        "ajax_referer_list": {
            "_value": []
        },
        "ajax_token_bypass_list": {
            "_value": []
        },
        "charset": {
            "_value": ""
        },
        "check_console_open": {
            "_value": False
        },
        "content_type_overwrite": {
            "_value": False
        },
        "disable_123456": {
            "_value": False
        },
        "disable_encoding_ajax_args": {
            "_value": False
        },
        "disable_upstream_keepalive": {
            "_value": True
        },
        "enableHttp2": {
            "_value": False
        },
        "enable_Accept_Encoding": {
            "_value": True
        },
        "enable_P3P_Options": {
            "_value": False
        },
        "enable_Request_Custom_Head": {
            "_value": False
        },
        "enable_Response_Custom_Head": {
            "_value": False
        },
        "enable_WL_Proxy_Client_IP": {
            "_value": False
        },
        "enable_X_Content_Type_Options": {
            "_value": False
        },
        "enable_X_Forwarded_For": {
            "_value": True
        },
        "enable_X_Real_IP": {
            "_value": True
        },
        "enable_X_XSS_Protection": {
            "_value": False
        },
        "enable_charset": {
            "_value": False
        },
        "enable_compatible_mode": {
            "_value": False
        },
        "enable_host": {
            "_value": False
        },
        "enable_http2https": {
            "_value": False
        },
        "enable_mobile_block_whitelist": {
            "_value": False
        },
        "enable_mobile_list": {
            "_value": False
        },
        "enable_mobile_protection": {
            "_value": False
        },
        "enable_webrtc": {
            "_value": False
        },
        "enable_x_frame_option": {
            "_value": False
        },
        "enabled": {
            "_value": True
        },
        "health_check": {
            "_value": {
                "health_check_interval": "5",
                "health_check_path": "/",
                "health_check_reset_times": "3",
                "health_check_timeouts": "5",
                "health_check_type": "tcp",
                "health_user_agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
                "is_health_check_enable": False
            }
        },
        "http2https_new_port": {
            "_value": "8080"
        },
        "http2https_org_port": {
            "_value": "80"
        },
        "ie_rendering_mode": {
            "_value": False
        },
        "internal_res_path": {
            "_value": "/"
        },
        "keep_http_version": {
            "_value": False
        },
        "learning_mode": {
            "_value": False
        },
        "limit_except": {
            "_value": [
                True,
                True,
                False,
                False,
                False,
                True,
                False,
                False,
                False
            ]
        },
        "load_balancing_strategy": {
            "_value": "ip_hash"
        },
        "mobile_config_version": {
            "_value": 4
        },
        "mobile_customer_id": {
            "_value": "None"
        },
        "mobile_enable_ignore_jsonp": {
            "_value": False
        },
        "mobile_enable_online_perceptron": {
            "_value": False
        },
        "mobile_only": {
            "_value": False
        },
        "mobile_passthrough_collection": {
            "_value": False
        },
        "mobile_protect_rules": {
            "_value": ""
        },
        "mobile_v1_process_mode": {
            "_value": "block"
        },
        "name": {
            "_value": "172.16.30.4"
        },
        "no_content_type": {
            "_value": False
        },
        "prevent_corejs_reentry": {
            "_value": False
        },
        "prevent_scanner": {
            "_value": False
        },
        "protected_list": {
            "_value": {
                "aiwaf_attack_interception": False,
                "ajax_request_body_encryption": False,
                "ajax_response_encryption": False,
                "automated_tool_intercept": True,
                "crack_behavior_interception": True,
                "injection_attack_interception": True,
                "mobile_sdk_protection": False,
                "web_advanced_protection": False,
                "web_standard_protection": True
            }
        },
        "proxy_connect_timeout": {
            "_value": ""
        },
        "proxy_read_timeout": {
            "_value": ""
        },
        "proxy_send_timeout": {
            "_value": ""
        },
        "proxy_ssl_ciphers": {
            "_value": "DEFAULT"
        },
        "proxy_ssl_protocols": {
            "_value": "SSLv3, TLSv1, TLSv1.1, TLSv1.2"
        },
        "reduce_level_of_protection_by_ua": {
            "_value": False
        },
        "reload_status_code": {
            "_value": "412"
        },
        "reserve_comment": {
            "_value": True
        },
        "rule_set": {
            "_value": "looseSet"
        },
        "scc": {
            "_value": {
                "enable": False,
                "text": ""
            }
        },
        "security_level_max": {
            "_value": [
                "bot",
                "cookie_token",
                "crack",
                "waf"
            ]
        },
        "security_level_min": {
            "_value": [
                "bot",
                "cookie_token",
                "crack",
                "waf"
            ]
        },
        "site_customize_name": {
            "_value": ""
        },
        "src_ip_from": {
            "_value": ""
        },
        "src_ip_use_global_setting": {
            "_value": True
        },
        "ssl_ciphers": {
            "_value": "kEECDH:!RC4:!eNULL:!aNULL:!DES:DES-CBC3-SHA"
        },
        "ssl_protocols": {
            "_value": "TLSv1, TLSv1.1, TLSv1.2, TLSv1.3"
        },
        "static_resource_list": {
            "_value": "7z,aac,amr,asm,avi,bak,bat,bmp,bin,c,cab,css,csv,com,cpp,dat,dll,doc,dot,docx,exe,eot,fla,flc,fon,fot,font,gdb,gif,gz,gho,hlp,hpp,htc,ico,ini,inf,ins,iso,js,jar,jpg,jpeg,json,java,lib,log,map,mid,mp4,mpa,m4a,mp3,mpg,mkv,mod,mov,mim,mpp,msi,mpeg,obj,ocx,ogg,olb,ole,otf,py,pyc,pas,pgm,ppm,pps,ppt,pdf,pptx,png,pic,pli,psd,qif,qtx,ra,rm,ram,rmvb,reg,res,rtf,rar,so,sbl,sfx,swa,swf,svg,sys,tar,taz,tif,tiff,torrent,txt,ttf,vsd,vss,vsw,vxd,woff,woff2,wmv,wma,wav,wps,xbm,xpm,xls,xlsx,xsl,xml,z,zip,apk,plist,ipa"
        },
        "useBuiltInCert": {
            "_value": False
        },
        "waf_add_disabled_set": {
            "_value": ""
        },
        "waf_custom_set_template": {
            "_value": "looseSet"
        },
        "waf_del_disabled_set": {
            "_value": ""
        },
        "waf_learning_mode": {
            "_value": False
        },
        "waf_rule_module_config": {
            "_value": {
                "sensitive_info_filter_interception": {
                    "action": "replace",
                    "skip_backend": 4,
                    "skip_forward": 3,
                    "target_name": "*"
                }
            }
        },
        "websocket_paths": {
            "_value": []
        },
        "x_frame_option_allow_uri": {
            "_value": ""
        },
        "xff_position": {
            "_value": "last"
        }
    }
}
parsedlog_export = {
    "address": {
        "_value": [{
                "ip": "10.10.10.10",
                "port": "1234",
                "proto": "kafka",
                "topic": "1111111"
            },
            {
                "ip": "10.10.10.10",
                "port": "1234",
                "proto": "kafka",
                "topic": "sdcx"
            },
            {
                "ip": "1.2.3.4",
                "port": "12345",
                "proto": "udp",
                "topic": ""
            }
        ]
    },
    "enabled": {
        "_value": 1
    },
    "external_level": {
        "_value": "debug"
    },
    "external_type": {
        "_value": "all"
    },
    "rr_mode": {
        "_value": 0
    }
}


def get_all(node):
    values = {}
    for key, value in node.items():
        print('key:{}'.format(key))
        print('value:{}'.format(value))

        if key.startswith('_'):
            print('ignore key:{}'.format(key))
            continue

        if value.get('_deleted') == 1:
            print('ignore value:{}'.format(value))
            continue
        v = value.get('_value')
        if v is None:
            print('call self')
            values[key] = get_all(value)
        else:
            print('get v:{}'.format(v))
            values[key] = v

    return values


# values = get_all(upstreams)
# print(json.dumps(values.values(), indent=2))    # python2.7 ok, python3 error, Object of type dict_values is not JSON serializable
# print(json.dumps(values, indent=2))

values = get_all(parsedlog_export)
print(json.dumps(values, indent=2))
