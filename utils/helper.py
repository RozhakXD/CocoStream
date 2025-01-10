import aiohttp, json, re, time

async def cocobox(video_urls: str) -> dict:
    async with aiohttp.ClientSession() as session:
        if 'surl=' in str(video_urls):
            find_surl = re.search(r'surl=([^/?]+)', str(video_urls))
            if find_surl != None:
                surl = (f'1{find_surl.group(1)}' if str(find_surl.group(1)[:1]) != '1' else find_surl.group(1))
            else:
                return {
                    'success': False,
                    'message': 'Tidak menemukan id video!'
                }
        elif '/s/' in str(video_urls):
            find_surl = re.search(r'/s/([^/?]+)', str(video_urls))
            if find_surl != None:
                surl = (f'1{find_surl.group(1)}' if str(find_surl.group(1)[:1]) != '1' else find_surl.group(1))
            else:
                return {
                    'success': False,
                    'message': 'Tidak menemukan id video!'
                }
        else:
            return {
                'success': False,
                'message': 'Hanya bisa mengunduh dari tautan surl=...!'
            }
        session.headers.update(
            {
                "Cookie": "ndus=YS-3n_3K27ciZ5k-ptkBSKQ6-Yr5HERyGjFyrG1v; STOKEN=dubox",
                "Content-Type": "application/x-www-form-urlencoded",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Host": "www.safepavo.com",
                "Referer": "https://www.safepavo.com",
                "User-Agent": "dubox;3.32.1;RMX3301;android-android;9;JSbridge1.0.10;jointbridge;1.1.39;"
            }
        )
        params = {
            "shorturl": f"{surl}",
            "clienttype": "0",
            "app_id": "250528",
            "dp-logid": "",
            "root": "1",
            "jsToken": "",
            "web": "1",
            "scene": "",
            "channel": "dubox",
        }
        async with session.get("https://www.safepavo.com/api/shorturlinfo", params=params) as response:
            text = await response.text()
            if '"shareid":' in str(text) and '"list":' in str(text):
                json_data = json.loads(text)
                shareid, uk, page = json_data['shareid'], json_data['uk'], json_data['page']
                results = []
                for data in json_data['list']:
                    fs_id = data['fs_id']
                    params = {
                        "devuid": "F8EB2EACAC5A89492CB762FB2E7C5BD4|VSH6QDQL7",
                        "shareid": f"{shareid}",
                        "uk": f"{uk}",
                        "page": f"{page}",
                        "needsublist": "1",
                        "sekey": "",
                        "fid": f"{fs_id}",
                        "sign": "",
                        "timestamp": f"{int(time.time())}",
                        "share_type": "100",
                        "bdstoken": "",
                        "clienttype": "1",
                        "channel": "android_9_RMX3301_bd-dubox_pavo_webpage",
                        "version": "5.5.8",
                        "logid": "",
                        "lang": "id_ID",
                        "versioncode": "55800",
                        "ZID": "",
                        "isVip": "0",
                        "bgstatus": "0",
                        "carrier_country": "id",
                        "device_country": "id",
                        "phone_brand": "realme",
                        "activestatus": "0",
                        "startDevTime": f"{int(time.time() * 1000)}",
                        "firstlaunchtime": f"{int(time.time()) - 3600}",
                        "time": "1722430798886",
                        "cuid": "",
                        "network_type": "wifi",
                        "apn_id": "1_0",
                        "carrier": "51001id_51001id",
                        "app_id": "20",
                        "app_name": "moder",
                        "af_media_source": "null",
                        "rand": "deb7d9d60cbb71cfcc70b7287c20f05deecb3054"
                    }
                    async with session.get(f"https://www.safepavo.com/share/list", params=params) as response2:
                        text = await response2.text()
                        if not '"dlink":""' in str(text) and '"list":' in str(text):
                            for data in json.loads(text)['list']:
                                server_filename = data.get('server_filename')
                                direct_link = data.get('dlink')
                                size = data.get('size')
                                size_mb = int(size) / (1024 * 1024) 
                                if direct_link and direct_link not in results:
                                    results.append(
                                        {
                                            'server_filename': server_filename,
                                            'direct_link': direct_link,
                                            'size': size_mb
                                        }
                                    )
                        else:
                            return {
                                'success': False,
                                'message': 'Tidak menemukan direct link!'
                            }
                if results:
                    return {
                        'success': True,
                        'message': 'Berhasil menemukan direct link!',
                        'download_links': results
                    }
                else:
                    return {
                        'success': False,
                        'message': 'Tidak menemukan direct link!'
                    }
            else:
                return {
                    'success': False,
                    'message': 'Tidak mendapatkan data dari tautan ini!'
                }