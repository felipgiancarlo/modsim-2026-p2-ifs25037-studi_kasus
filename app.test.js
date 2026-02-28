const { callAxios } = require("./_utils");
const { baseUrl } = require("./_config");

describe("Website Checking", () => {
  test("valid: website dapat diakses", async () => {
    const res = await callAxios("get", baseUrl);
    expect(res.status).toBe(200);
  });
});
