nama_toko = "PENYEWAAN ALAT CAMPING"
maks_percobaan = 3

katalog = {
    "TND1": {"nama": "Tenda Dome 2P", "harga": 35000, "stok": 5, "kategori": "Tenda"},
    "SBG1": {"nama": "Sleeping Bag", "harga": 15000, "stok": 10, "kategori": "Tidur"},
    "KMP1": {"nama": "Kompor Portable", "harga": 20000, "stok": 6, "kategori": "Masak"},
    "HDM1": {"nama": "Headlamp LED", "harga": 10000, "stok": 8, "kategori": "Penerangan"},
}

aturan = ("KTP/KTM wajib ditinggal", "Maksimal sewa 7 hari", "Cek kondisi alat saat kembali")

akun = {
    "admin": {"password": "admin123", "peran": "admin"},
}

riwayat = []

rupiah = lambda angka: "Rp" + str(angka)

def input_angka(pesan):
    try:
        return int(input(pesan))
    except ValueError:
        print("Input harus berupa angka bulat")
        return None

def tampilkan_katalog(semua=False):
    print("\nDAFTAR ALAT CAMPING")
    for kode, info in katalog.items():
        if semua or info["stok"] > 0:
            print(f"[{kode}] {info['nama']} | {rupiah(info['harga'])}/hari | "
                  f"{info['kategori']} | Stok {info['stok']}")

def hitung_diskon(total, hari):
    if hari >= 3:
        return total * 10 // 100
    else:
        return 0

def login():
    print("\nLOGIN")
    for percobaan in range(1, maks_percobaan + 1):
        username = input("Username: ").strip().lower()
        password = input("Password: ")
        data = akun.get(username)

        if data is not None and data["password"] == password:
            print(f"Login berhasil! Selamat datang, {username} ({data['peran']})")
            return username, data["peran"]

        sisa = maks_percobaan - percobaan
        if sisa > 0:
            print(f"Username atau password salah. Sisa percobaan: {sisa}")

    print("Login gagal 3 kali. Kembali ke menu awal.")
    return None, None

def daftar_akun(peran="user"):
    print("\nDAFTAR AKUN BARU")
    username = input("Username baru: ").strip().lower()

    if not username.isalpha():
        print("Username hanya boleh berisi huruf (tanpa angka, spasi, atau simbol)")
    elif username in akun:
        print("Username sudah dipakai")
    else:
        password = input("Password (min 6 karakter): ")
        if len(password) < 6:
            print("Password terlalu pendek")
        else:
            akun[username] = {"password": password, "peran": peran}
            print("Akun berhasil dibuat, silakan login")

def tampilkan_akun():
    print("\nDAFTAR AKUN")
    for nama_akun, data in akun.items():
        print(f"- {nama_akun} ({data['peran']})")

def cetak_ringkasan(username, keranjang, kategori_disewa):
    print("\nRINGKASAN PENYEWAAN")

    if not keranjang:
        print("Keranjang kosong, tidak ada penyewaan")
        return

    hari_terlama = 0
    total = 0
    for item in keranjang:
        print(f"- {item[2]}x {item[1]} ({item[3]} hari): {rupiah(item[4])}")
        total = total + item[4]
        if item[3] > hari_terlama:
            hari_terlama = item[3]

    diskon = hitung_diskon(total, hari_terlama)
    grand_total = total - diskon

    semua_kategori = set()
    for info in katalog.values():
        semua_kategori.add(info["kategori"])
    belum = semua_kategori - kategori_disewa

    print("Penyewa              :", username)
    print("Kategori disewa      :", ", ".join(sorted(kategori_disewa)))
    if len(belum) == 0:
        print("Kategori belum disewa: -")
    else:
        print("Kategori belum disewa:", ", ".join(sorted(belum)))
    print("Subtotal             :", rupiah(total))
    print("Diskon (sewa >=3 hr) : -" + rupiah(diskon))
    print("Total bayar          :", rupiah(grand_total))

    rata_hari = int(grand_total / hari_terlama)
    print("Rata-rata per hari   :", rupiah(rata_hari))

    riwayat.append({
        "user": username,
        "item": len(keranjang),
        "total": grand_total,
    })

    try:
        orang = int(input("\nDibayar berapa orang (patungan)? "))
        if orang < 0:
            print("Jumlah orang tidak boleh negatif")
        else:
            per_orang = grand_total // orang
            sisa = grand_total % orang
            print("Per orang :", rupiah(per_orang))
            print("Sisa      :", rupiah(sisa))
    except ValueError:
        print("Jumlah orang harus berupa angka bulat")
    except ZeroDivisionError:
        print("Jumlah orang tidak boleh 0")

def menu_user(username):
    keranjang = []
    kategori_disewa = set()

    while True:
        print(f"\n--- {nama_toko} | User: {username} ---")
        print("1. Lihat Katalog & Sewa Alat")
        print("2. Lihat Aturan Sewa")
        print("3. Batalkan Item Terakhir")
        print("4. Selesai & Cetak Ringkasan")
        print("5. Logout (transaksi dibatalkan)")
        pilihan = input("Pilih menu (1-5): ")

        if pilihan == "1":
            tampilkan_katalog()
            kode = input("Masukkan kode alat (atau 'batal'): ").upper()

            if kode == "BATAL" or kode == "":
                print("Penyewaan dibatalkan")
            else:
                try:
                    alat = katalog[kode]
                    jumlah = int(input("Jumlah unit disewa: "))
                    hari = int(input("Lama sewa (hari): "))

                    valid = jumlah > 0 and hari > 0 and hari <= 7
                    if not valid:
                        print("Jumlah harus lebih dari 0 dan lama sewa 1-7 hari")
                    elif jumlah > alat["stok"]:
                        print("Stok tidak cukup! Sisa stok:", alat["stok"])
                    else:
                        alat["stok"] = alat["stok"] - jumlah
                        subtotal = alat["harga"] * jumlah * hari
                        keranjang.append((kode, alat["nama"], jumlah, hari, subtotal))
                        kategori_disewa.add(alat["kategori"])
                        print(f"Berhasil: {jumlah}x {alat['nama']} ({hari} hari) = {rupiah(subtotal)}")
                except KeyError:
                    print("Kode alat tidak ditemukan")
                except ValueError:
                    print("Jumlah dan hari harus berupa angka bulat")

        elif pilihan == "2":
            print("\nATURAN SEWA")
            nomor = 1
            for isi in aturan:
                print(nomor, ".", isi)
                nomor += 1

        elif pilihan == "3":
            if not keranjang:
                print("Keranjang masih kosong")
            else:
                item = keranjang.pop()
                katalog[item[0]]["stok"] = katalog[item[0]]["stok"] + item[2]
                kategori_disewa = set()
                for sisa in keranjang:
                    kategori_disewa.add(katalog[sisa[0]]["kategori"])
                print("Item dibatalkan:", item[2], "x", item[1])

        elif pilihan == "4":
            cetak_ringkasan(username, keranjang, kategori_disewa)
            return

        elif pilihan == "5":
            for item in keranjang:
                katalog[item[0]]["stok"] += item[2]
            if keranjang:
                print("Transaksi dibatalkan, stok dikembalikan")
            print("Logout berhasil")
            return

        else:
            print("Menu tidak valid, pilih 1-5")

def menu_admin(username):
    while True:
        print(f"\n--- PANEL ADMIN | {username} ---")
        print("1. Lihat Semua Alat")
        print("2. Tambah Alat Baru")
        print("3. Tambah Stok Alat")
        print("4. Ubah Harga Alat")
        print("5. Lihat Riwayat Transaksi")
        print("6. Lihat Daftar Akun")
        print("7. Hapus Alat")
        print("8. Hapus Akun User/Admin")
        print("9. Tambah Akun Baru (user/admin)")
        print("10. Logout")
        pilihan = input("Pilih menu (1-10): ")

        if pilihan == "1":
            tampilkan_katalog(semua=True)

        elif pilihan == "2":
            kode = input("Kode alat baru (contoh: LTR1): ").strip().upper()
            if kode == "" or kode in katalog:
                print("Kode kosong atau sudah dipakai")
            else:
                nama = input("Nama alat: ").strip()
                kategori = input("Kategori: ").strip().title()
                harga = input_angka("Harga per hari: ")
                stok = input_angka("Stok awal: ")
                if nama == "" or kategori == "":
                    print("Nama dan kategori tidak boleh kosong")
                elif harga is None or stok is None or harga <= 0 or stok < 0:
                    print("Harga harus > 0 dan stok tidak boleh negatif")
                else:
                    katalog[kode] = {"nama": nama, "harga": harga, "stok": stok, "kategori": kategori}
                    print("Alat berhasil ditambahkan:", nama)

        elif pilihan == "3":
            tampilkan_katalog(semua=True)
            kode = input("Kode alat: ").strip().upper()
            if kode not in katalog:
                print("Kode alat tidak ditemukan")
            else:
                tambah = input_angka("Jumlah stok ditambah: ")
                if tambah is not None and tambah > 0:
                    katalog[kode]["stok"] += tambah
                    print(f"Stok {katalog[kode]['nama']} sekarang {katalog[kode]['stok']}")
                elif tambah is not None:
                    print("Jumlah harus lebih dari 0")

        elif pilihan == "4":
            tampilkan_katalog(semua=True)
            kode = input("Kode alat: ").strip().upper()
            if kode not in katalog:
                print("Kode alat tidak ditemukan")
            else:
                harga = input_angka("Harga baru per hari: ")
                if harga is not None and harga > 0:
                    katalog[kode]["harga"] = harga
                    print(f"Harga {katalog[kode]['nama']} sekarang {rupiah(harga)}/hari")
                elif harga is not None:
                    print("Harga harus lebih dari 0")

        elif pilihan == "5":
            print("\nRIWAYAT TRANSAKSI")
            if not riwayat:
                print("Belum ada transaksi")
            else:
                pendapatan = 0
                nomor = 1
                for t in riwayat:
                    print(f"{nomor}. {t['user']} | {t['item']} item | {rupiah(t['total'])}")
                    pendapatan += t["total"]
                    nomor += 1
                print("Total pendapatan:", rupiah(pendapatan))

        elif pilihan == "6":
            tampilkan_akun()

        elif pilihan == "7":
            tampilkan_katalog(semua=True)
            kode = input("Kode alat yang dihapus: ").strip().upper()
            if kode not in katalog:
                print("Kode alat tidak ditemukan")
            else:
                yakin = input(f"Yakin hapus {katalog[kode]['nama']}? (y/n): ").strip().lower()
                if yakin == "y":
                    del katalog[kode]
                    print("Alat berhasil dihapus")
                else:
                    print("Penghapusan dibatalkan")

        elif pilihan == "8":
            tampilkan_akun()
            target = input("Username yang dihapus: ").strip().lower()
            if target not in akun:
                print("Username tidak ditemukan")
            elif target == username:
                print("Akun yang sedang dipakai tidak bisa dihapus")
            else:
                yakin = input(f"Yakin hapus akun {target}? (y/n): ").strip().lower()
                if yakin == "y":
                    del akun[target]
                    print("Akun berhasil dihapus")
                else:
                    print("Penghapusan dibatalkan")

        elif pilihan == "9":
            peran_baru = input("Peran akun baru (admin/user): ").strip().lower()
            if peran_baru == "admin" or peran_baru == "user":
                daftar_akun(peran_baru)
            else:
                print("Peran harus 'admin' atau 'user'")

        elif pilihan == "10":
            print("Logout berhasil")
            return

        else:
            print("Menu tidak valid, pilih 1-10")

while True:
    print(f"\n____{nama_toko}____")
    print("1. Login")
    print("2. Daftar Akun Baru")
    print("3. Keluar")
    awal = input("Pilih menu (1-3): ")

    if awal == "1":
        user_aktif, peran = login()
        if peran == "admin":
            menu_admin(user_aktif)
        elif peran == "user":
            menu_user(user_aktif)
    elif awal == "2":
        daftar_akun()
    elif awal == "3":
        print("Terima kasih, sampai jumpa!")
        break
    else:
        print("Menu tidak valid, pilih 1-3")

    #milik kelompok 3 | penyewaan alat camping