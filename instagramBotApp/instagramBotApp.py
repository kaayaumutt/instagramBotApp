from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from instagramConfig import *
import time 

class Instagram:
    """
        _signIn_ = Logged in instagram account.
        _myFollowers_ = My followers listed and writing file.
        _myFollowings_ = My followings listed and writing file.
        _followingUsers_ = Follow my targeted users and save screenshot.
        _followingUsers_ = Unfollow my targeted users and save screenshot.
        _otoMessage_ = Automatic reply for new messages.
    """
    def __init__(self,browser,userName,password,follow="",followingUsers="",unfollowingUsers="",otoMessage=""):
        self.browser = browser
        self.userName = userName
        self.password = password
        self.follow = follow
        self.followingUsers = followingUsers
        self.unfollowingUsers = unfollowingUsers
        self.otoMessage = otoMessage
    
    def _signIn_(self):
        self.browser.get("https://www.instagram.com/accounts/login/")
        self.browser.maximize_window()
        time.sleep(2)
        emailInput = self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
        passwordInput = self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")
        emailInput.send_keys(self.userName)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(5)

    def _myFollowers_(self):
        self._signIn_()
        self.browser.get(f"https://www.instagram.com/{self.userName}")
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(2)
        dialog = self.browser.find_element_by_css_selector("div._1XyCr")
        txtname = "my_followers.txt"
        self._followControl_(dialog,txtname)

    def _myFollowings_(self):
        self._signIn_()
        self.browser.get(f"https://www.instagram.com/{self.userName}")
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click()
        time.sleep(2)
        dialog = self.browser.find_element_by_css_selector("div.isgrP")
        txtname = "my_followings.txt"
        self._followControl_(dialog,txtname)

    def _followControl_(self,dialog,txtname):
        followerCount = len(dialog.find_elements_by_css_selector("li"))
        print(f"İlk değer: {followerCount}")
        action = webdriver.ActionChains(self.browser)

        while True:
            dialog.click()
            for i in range(3):
                action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(2)
            newCount = len(dialog.find_elements_by_css_selector("li"))
            if followerCount != newCount:
                followerCount = newCount
                print(f"Yeni değer: {newCount}")
                time.sleep(1)
            else:
                break
        
        followers = dialog.find_elements_by_css_selector("li")
        time.sleep(2)

        followerList = []
        for user in followers:
            link = user.find_element_by_css_selector("a").get_attribute("href")
            print(link)
            followerList.append(link)
        
        with open(txtname,"w",encoding="UTF-8") as file:
            for item in followerList:
                file.write(item+"\n")

    def _followingUsers_(self):
        self._signIn_()
        for users in self.followingUsers:
            self.browser.get(f"https://www.instagram.com/{users}")
            time.sleep(2)
            followName = self.browser.find_element_by_class_name("vBF20")
            if followName.text == self.follow:
                followName.click()
                time.sleep(1)
                self.browser.save_screenshot(f"{users} follow.png")
                print(f"{users} sayfasını başarıyla takip ettiniz..")
                time.sleep(2)
            else:
                print(f"{users} zaten Takip Ediyorsun..")
                self.browser.save_screenshot(f"{users} follow.png")
                time.sleep(2)

    def _unFollowingUsers_(self):
        self._signIn_()
        for users in self.unfollowingUsers:
            self.browser.get(f"https://www.instagram.com/{users}")
            time.sleep(2)
            followName = self.browser.find_element_by_class_name("vBF20")
            if followName.text != self.follow:
                followName.click()
                time.sleep(2)
                exit = self.browser.find_element_by_css_selector("button.aOOlW.-Cab_")
                exit.click()
                time.sleep(1)
                self.browser.save_screenshot(f"{users} unfollow.png")
                print(f"{users} sayfasını başarıyla takip etmeyi bıraktınız..")
                time.sleep(2)
            else:
                print(f"{users} sayfasını zaten Takip Etmiyorsun..")
                self.browser.save_screenshot(f"{users} unfollow.png")
                time.sleep(2)

    def _otoMessage_(self):
        self._signIn_()
        self.browser.get("https://www.instagram.com/direct/inbox/")
        time.sleep(5)
        exit = self.browser.find_element_by_css_selector("button.aOOlW.HoLwm")
        exit.click()
        time.sleep(5)
        getlist = self.browser.find_elements_by_css_selector("div.DPiy6.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm")
        messageCount = 0
        action = webdriver.ActionChains(self.browser)
        firstCount = len(getlist)
        for list in getlist:
            try:
                newMessage = list.find_element_by_css_selector("span._7UhW9.xLCgt.qyrsm.KV-D4.se6yk")
                time.sleep(2)
                newMessage.click()
                messageCount +=1
                messageInput = self.browser.find_element_by_xpath("//*[@id='react-root']/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
                messageInput.send_keys(self.otoMessage)
                messageInput.send_keys(Keys.ENTER)
                time.sleep(5)
                messageControl = 0
                if messageCount>=6:
                    messageCount=0
                    messageBox = self.browser.find_element_by_css_selector("div._7WGDw")
                    messageBox.click()
                    time.sleep(3)
                    while True:
                        messageBox.click()
                        action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                        newCount = len(getlist)
                        if newCount>firstCount:
                            newCount=firstCount
                            print(f"Okunan toplam msj sayın: {newCount}")
                            break
                        if newCount == firstCount:
                            messageControl+=1
                            if messageControl == 3:
                                print(f"Okunan toplam msj sayın: {newCount}")
                                break
                    time.sleep(2)
            except:
                messageCount +=1


instagram = Instagram(browser,userName,password,follow,followingUsers,unfollowingUsers,otoMessage)

if __name__=="main":
    print(instagram.__doc__)
else:
    print("instagramBotApp.py dosyası başka dosyadan çalışıyor.")

#-Settings -> instagramConfig.py