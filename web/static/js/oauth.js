var AUTH = {
    vk: {
        auth: function(f) {
            VK.Auth.getLoginStatus(function(response) {
                if (response.session) {
                    f(true);
                }
                else {
                    f(false);
                }
            });
        },
        call_login: function(response) {
            if (response.status == "connected") {
                console.log(response);
                window.location = PUBAUTH_COMPLETE;
            }
        },
        login: function() {
            var self = this;
            VK.Auth.login(self.call_login);
        },
        logout: function() {
            VK.Auth.getLoginStatus(self.call_login);
        }
    }
};