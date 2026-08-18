# -*- coding: utf-8 -*-
# HKD OBFUSCATE v4 - portable source payload, no marshal/code-object dependency.
# Protection is import-time only; protected functions have no per-call wrapper.
def _hkd_v4_bootstrap(_g):
    import binascii as _hb
    import hashlib as _hh
    import struct as _hs
    import zlib as _hz

    _b = (
        _hb.unhexlify('aa7205657696d7b77f331561bca504e60754cdfe0bd55572d7ac6899c409978052bbb1409e4db813d319f9b9636b4e8602351cd51e36b025b789dc2ec61f40ec94d8e06ac690de3853e053c65a18b42da5ff161d59604b817b8f435111d971cbf1f6641320e65cb40a666b80dd730af5c81a9cf1e0edfeb152c497231cb067fa'),
        _hb.unhexlify('4ba26778c715c669b11ac6b6a1f3ae33d6a3365bd58ab77a588d725496b6773e20117f7090cd84d5a5176c5c703faf69d87d312c5eed88895b2d77f30283a01c2dfcb9b320cc6ddaf4691d01b31de565695478318fe1bca3327cca345e776f9973fa9bfffdd0da6d5ab8d1795cadb8478b72cbed49d8c1b23b518805c51e00b0'),
        _hb.unhexlify('f0c8fc56d0a751c2426360b4d7606ec23c49e9fa8d0bdfd02047d804236e94f1936eb923dbf467fd574ced17100ae744bbc03ed2ac89980fa105bc331fe320cfb3087c81f6403b234cbab1fc9186d929e14833ca5f06785fe61f4d7e74494d82d15ec4cb65c5c0a804fa7fd08a23c33467a29604eed614a99315cce4d83d9630'),
        _hb.unhexlify('72bb5b118b35233e95fd456571842c9b210a8258b437ec0ad89e1836cb8fb2d09d5af33a4b7946fa7914ac3ec6448931367b766e1438b9e362f8ad8c7296a97bb5a87ba9acfc3f16b224ab838c2690281c8a962e7308833fc6c5aee74bf9846c204cf939dd2c81c8f3541bbc2c07364f1fd905184ecae7b171313a689b0f359e'),
        _hb.unhexlify('e603542da5762396590438ed62bd7c64303fe34e283dc731e81f8f6a001fc2b97d52a34865c18e0035f00b68125f904211a718ead3d268054541d2ae777d1f32f08c92a839cf06c8897bad15c73751e44e6ae45d489a5801bdebd6d743108e20943622d80ed955e2e88da168c0ea35e0ece3c1a2962ffd14972edfb51e8997c1'),
        _hb.unhexlify('6b34a0562bae71c9281ffd9f1e7e474b053d18b116cdc4b3a00678f3da0141cf1ccbf40613600514a86abcb99ea6aeca37e53f910a0863dc7639f05779d72495037020'),
        _hb.unhexlify('dada4facf933f4b628c14c4e8afb8839ad184eae1b8a13c5e567784548270ed92fd0ca72dc3c605b12e82a06527aa423987be4b107bfd0dde973666970ffbe50d996b31741aeb154eb88af3914120ffa8680a41d1ae8a26505eae8640034df8c9710bda1ce04e5c806d2124b198825d03d9d5c998ec01a1c5160eb2d215a1e01'),
        _hb.unhexlify('d25a1eca873602b53039ca9f345de9e79dfc2727cc058de4e45492a1e5258b085ed2b8daa7af129b5aa6104f7a0a1d6298dd6c8c66a75235f9b23fc89e85408590b1b6b6a9b6cfaeee33c578e3b2514a6b659e2fb7ca19a8027db0364a8eff1a7e1e9c7cc54e87c29e6d3311b515a2fe8f63b607fadd667a48c107a90d18e033'),
        _hb.unhexlify('7c677192323eb3e471c456dd732e116d3c7d7e005ebcd24982e50e1462959d93132fef517f54e34875205c08806d23068cbc672c9fad57d924f73d4b8068b5b96c28a70818bb4511e28b52fe3f183998fe06d39bf26bc4d240dbed37dc371609c34b69697ceae7357a27c6d7b10eea6b3d337ae37d4e13041ea0e12cf1efffeb'),
        _hb.unhexlify('fc2bd3263ca08d9172c2d74264315777bca8c290da7844efe6b5315cb2c3e5d7b162e04ea30e2d3e69c21cc0d621360c976be92d31359a4968bf704f6779978ea9dcea93337de36134c0e1ad14d5db1d6e81f4e5ec1685b916250fbe0318f1aa21920a7d6311f9dd2ff1f79a9069b76c9ba83566c82f4cec73470de6103a5651'),
        _hb.unhexlify('fafb53274b51ca5913d3b8c9cb82d58ae94e438ce00295961fddc592625f9f057618028b980724dce08ec2910f517fb7ff031037c2bc7089064a2613454cbcdf3b24696a764250c15946501588b5556ab53011023bb82a2f26afbd998e5fa7ae2016f03e5087dd2c65fdfbecb768c6d8673d4c07fa82da22fdbff3e3598a6291'),
        _hb.unhexlify('5cdf094a1b58ee04894de67fbd0c6863b660de4f8bbb6927b3e4161ed1c113b50e303e245541c5c4b44f6b0f7fe2282d351ea8c5ed36ec13983b984e5f8d93ab3573bf88cb39ff4bd66a675e42c941e38a85dbf89635436d0056bdaae54e8a03d5de573e0763b5d1a0e75443f4efeada8bb4dc561d04a077d5112f2a3e3b71f8'),
        _hb.unhexlify('23a249eec4ad8df9470c85e4436768e8aae57b7089344d3f4307cd947c27fd1f78bacd068b5d535f9a46410dee679a1a39727456e3fd02067e099ad93d382f0c92dcb90bf7a0ac58cddb040571127160470e4bd53bba946f13d9a18508727aeeb6d38cbccef26d67f51bb364e82514d053ad55053515668b065d2cd843988c40'),
    )
    _inv = (0, 1, 12, 8, 6, 2, 4, 7, 10, 11, 3, 9, 5)
    _leaves = (
        _hb.unhexlify('c6eec6856565a8d2c26040d80000a530a9b15014632f97658eb39277f3a054c4'),
        _hb.unhexlify('28bcf5e6ed22a7832fbcf1e4fc728b7fbdd24176ff6fca8c758be7d824fa0054'),
        _hb.unhexlify('25f8257a518c87a49c63cdd511515468078b802558c81562c19771cd614f78f0'),
        _hb.unhexlify('cb05084ba93ecd95b243f8cc756b28b38604579ad0859251447ff2d4e19f485c'),
        _hb.unhexlify('25ac147dd8c552145a060e2c503683fc2c6866496a4d4145af9d15421f81200f'),
        _hb.unhexlify('bfec73405f0b6b0f8c3b8b9a60d4c4b6c476e24f59b53c8ebd8d460555643324'),
        _hb.unhexlify('64315476d216b5456f62dde4e269d7dbbd7d0f2a04c2349b86146eac24f7bf9f'),
        _hb.unhexlify('e5d3ab3d1d63e8d34d81dcce35f885f9eb875639eafc17f31ca3164b2b99ef4e'),
        _hb.unhexlify('566b0c1b6bacdc62fa69909a43f40ac6df4c4e6b77af49fa9b447ca1b793329e'),
        _hb.unhexlify('f4e4f573799e54127ee30f811ec30f86e5518e5d9b063f97795f0609050f497a'),
        _hb.unhexlify('de4ee713455979fcafa07c1a66259e9f868a0f1c19a505e33383cfcc939cd789'),
        _hb.unhexlify('c3377ee978f2df0add77aa36643d9ac11950707d89d3e90536c058526852e7b0'),
        _hb.unhexlify('199dc0268f0ca0cd6d430c2b54277608c2c68e56cc90fa42495d33ebfd94aa63'),
    )
    _root = _hb.unhexlify('dba01869244938c306fbb670eb0553eaadde35f9da5d4fe81344921a98a5ec48')
    _share1 = _hb.unhexlify('55eda5f163d89abc0fa9ee2f50360fb8a1798cbdee89b7724aa601d666ef165c')
    _share2 = _hb.unhexlify('9f79c9c5af812421529d38fa0edc11dc26853438e917cd18eb1ba098b56c4e3b')

    def _u32(_n):
        return _hs.pack('>I', _n)

    def _xor(_a, _c):
        _o = bytearray(len(_a))
        _i = 0
        while _i < len(_a):
            _o[_i] = _a[_i] ^ _c[_i]
            _i += 1
        return bytes(_o)

    def _ks(_key, _index, _length):
        _o = bytearray()
        _counter = 0
        _seed = _key + _u32(_index)
        while len(_o) < _length:
            _o.extend(_hh.sha256(_seed + _u32(_counter)).digest())
            _counter += 1
        return bytes(_o[:_length])

    def _merkle(_values):
        if not _values:
            return _hh.sha256(b'').digest()
        _level = list(_values)
        while len(_level) > 1:
            if len(_level) & 1:
                _level.append(_level[-1])
            _next = []
            _i = 0
            while _i < len(_level):
                _next.append(_hh.sha256(_level[_i] + _level[_i + 1]).digest())
                _i += 2
            _level = _next
        return _level[0]

    _key = _xor(_share1, _share2)
    _parts = []
    _verify = []
    _i = 0
    while _i < len(_inv):
        _masked = _b[_inv[_i]]
        _raw = _xor(_masked, _ks(_key, _i, len(_masked)))
        _parts.append(_raw)
        _verify.append(_hh.sha256(_u32(_i) + _raw).digest())
        _i += 1

    if tuple(_verify) != _leaves or _merkle(_verify) != _root:
        raise ImportError('HKD protected payload integrity verification failed')

    try:
        _source = _hz.decompress(b''.join(_parts)).decode('utf-8')
    except Exception as _exc:
        raise ImportError('HKD protected payload reconstruction failed: %s' % (_exc,))

    _filename = _g.get('__file__') or '<HKD-obfuscated>'
    _code = compile(_source, _filename, 'exec', 0, True, 0)

    # Discard the plaintext string before running user code.  CPython may reclaim
    # it immediately; no plaintext source is retained as a module global.
    del _source

    # Exact module semantics: definitions execute in the actual module globals.
    exec(_code, _g, _g)

_hkd_v4_bootstrap(globals())
del _hkd_v4_bootstrap
